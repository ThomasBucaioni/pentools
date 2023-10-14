# Cross-compilation

## Mingw-w64 cross-compiler

### Install

```
sudo apt-get install mingw-w64
```

### Usage

Depending on the architecture of the processor:
```
i686-w64-mingw32-gcc some_exploit_source_code.c -o some_exploit.exe
i686-w64-mingw32-gcc some_exploit_source_code.c -lws2_32 -o some_exploit.exe
```
or (see [Service Hijacking](https://github.com/ThomasBucaioni/pentools/blob/main/microsoft/escalation.md#manual-hijacking-useraddc-code))
```
x86_64-w64-mingw32-gcc adduser.c -o adduser.exe
```

