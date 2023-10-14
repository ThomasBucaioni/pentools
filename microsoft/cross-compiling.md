# Cross-compilation

## Mingw-w64 cross-compiler

### Install

```
sudo apt-get install mingw-w64
```

### Usage

```
i686-w64-mingw32-gcc some_exploit_source_code.c -o some_exploit.exe
i686-w64-mingw32-gcc some_exploit_source_code.c -lws2_32 -o some_exploit.exe
```

