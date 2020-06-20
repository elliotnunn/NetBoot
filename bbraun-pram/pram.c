scal void read_extended_PRAM(char * where, const short size) =
{ 0x4280, 0x301F, 0x4840, 0x205F, 0xA051  };

pascal void write_extended_PRAM
        (const char * where, const short offset, const short size) =
{0x201F, 0x205F, 0xA052};

