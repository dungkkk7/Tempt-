import "pe"

rule suspiciousUnpack {
   meta:
      description = "Detects suspiciousUnpack.exe"
   strings:

      $unique2 = "Debugger Detected" fullword wide


   condition:
      uint16(0) == 0x5a4d and filesize < 100KB and
       $unique2
}

rule suspicious {
   meta:
      description = "Detects suspicious.exe"
   strings:

      $api2 = "IsDebuggerP" fullword ascii


   condition:
      uint16(0) == 0x5a4d and filesize < 80KB and
      1 of them
}