from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": ["tkinter", "unittest", "email"],
    "zip_include_packages": ["encodings", "PySide6", "shiboken6"],
    "includes": [],
    "include_files": ["Icons", "data"],
}

setup(
    name="ASMtoSENAITE",
    version="0.1.1",
    description="Middleware transferring ASTM Message to SENAITE LIMS",
    author="Berchie Agyemang Nti",
    options={"build_exe": build_exe_options},
    executables=[Executable("MDI/mdi_main_window.py", base="gui", target_name="ASTMtoSENAITE",
                            icon="port.ico", copyright="Copyright © 2024, BNITM.")],
)
