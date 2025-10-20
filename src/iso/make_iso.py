import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Iterable, Tuple


class ISOBuilder:
    def __init__(self, volume_id: str = "MY_ISO", publisher: Optional[str] = None):
        self.volume_id = volume_id
        self.publisher = publisher
        self._entries: list[Tuple[str, str]] = []

    def add_file(self, local_path: str, iso_dest_path: str):
        p = Path(local_path)
        if not p.is_file():
            raise FileNotFoundError(f"File not found: {local_path}")
        iso_dest_path = iso_dest_path.strip("/")
        self._entries.append((str(p.resolve()), iso_dest_path))

    def add_bytes(self, content: bytes, iso_dest_path: str):
        iso_dest_path = iso_dest_path.strip("/")
        tmp = tempfile.NamedTemporaryFile(delete=False)
        try:
            tmp.write(content)
            tmp.flush()
            tmp.close()
            self._entries.append((tmp.name, iso_dest_path))
        except Exception:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass
            raise

    def add_directory(self, local_dir: str, iso_dest_dir: str = "", recursive: bool = True):
        d = Path(local_dir)
        if not d.is_dir():
            raise FileNotFoundError(f"Directory not found: {local_dir}")
        iso_dest_dir = iso_dest_dir.strip("/")

        if recursive:
            for root, dirs, files in os.walk(d):
                relroot = os.path.relpath(root, d)
                for f in files:
                    src = os.path.join(root, f)
                    if relroot == ".":
                        dest = os.path.join(iso_dest_dir, f) if iso_dest_dir else f
                    else:
                        dest = os.path.join(iso_dest_dir, relroot, f) if iso_dest_dir else os.path.join(relroot, f)
                    self._entries.append((src, dest.replace("\\", "/")))
        else:
            for entry in d.iterdir():
                if entry.is_file():
                    dest = os.path.join(iso_dest_dir, entry.name) if iso_dest_dir else entry.name
                    self._entries.append((str(entry.resolve()), dest.replace("\\", "/")))

    def _find_mkisofs_like(self) -> Optional[Tuple[str, list]]:
        candidates = [
            ("xorriso", ["-as", "mkisofs", "-o"]),  # xorriso -as mkisofs -o out.iso [opts] <source>
            ("genisoimage", ["-o"]),               # genisoimage -o out.iso [opts] <source>
            ("mkisofs", ["-o"]),                   # mkisofs -o out.iso [opts] <source>
        ]
        for cmd, tmpl in candidates:
            if shutil.which(cmd):
                return cmd, tmpl
        return None

    def write(self,
              output_iso: str,
              joliet: bool = True,
              rock_ridge: bool = True,
              el_torito: Optional[Tuple[str, str, Iterable[str]]] = None,
              extra_cmdline_args: Optional[Iterable[str]] = None,
              cleanup_temp: bool = True) -> str:
        tool = self._find_mkisofs_like()
        if not tool:
            raise EnvironmentError("error")

        cmd_name, tmpl = tool
        workdir = tempfile.mkdtemp(prefix="isobuilder_")
        try:
            for src, dest in self._entries:
                dest_full = os.path.join(workdir, dest)
                os.makedirs(os.path.dirname(dest_full), exist_ok=True)
                shutil.copy2(src, dest_full)

            out_abs = str(Path(output_iso).expanduser().resolve())
            cmd = [cmd_name] + tmpl  # base
            cmd.append(out_abs)

            # common flags depending on tool
            # -J : Joliet (Windows long names), -R : Rock Ridge (POSIX perms)
            if "xorriso" in cmd_name:
                # when using xorriso -as mkisofs we pass the mkisofs-like options after -as mkisofs
                # already handled by tmpl
                if joliet:
                    cmd += ["-J"]
                if rock_ridge:
                    cmd += ["-R"]
                if self.volume_id:
                    cmd += ["-V", self.volume_id]
                if self.publisher:
                    cmd += ["-publisher", self.publisher]
            else:
                # genisoimage / mkisofs
                if joliet:
                    cmd += ["-J"]
                if rock_ridge:
                    cmd += ["-R"]
                if self.volume_id:
                    cmd += ["-V", self.volume_id]
                if self.publisher:
                    cmd += ["-publisher", self.publisher]

            if el_torito:
                boot_img, boot_cat, extra = el_torito
                cmd += ["-b", boot_img, "-c", boot_cat]
                cmd += list(extra)

            if extra_cmdline_args:
                cmd += list(extra_cmdline_args)

            cmd.append(workdir)

            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if proc.returncode != 0:
                raise RuntimeError(f"ISO 制作失败，命令：{' '.join(cmd)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")

            return out_abs
        finally:
            if cleanup_temp:
                try:
                    shutil.rmtree(workdir)
                except Exception:
                    pass
