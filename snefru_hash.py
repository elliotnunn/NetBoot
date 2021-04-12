#!/usr/bin/env python3

import struct

SBOXES = [
    [
        0x64F9001B, 0xFEDDCDF6, 0x7C8FF1E2, 0x11D71514, 0x8B8C18D3, 0xDDDF881E, 0x6EAB5056, 0x88CED8E1,
        0x49148959, 0x69C56FD5, 0xB7994F03, 0x0FBCEE3E, 0x3C264940, 0x21557E58, 0xE14B3FC2, 0x2E5CF591,
        0xDCEFF8CE, 0x092A1648, 0xBE812936, 0xFF7B0C6A, 0xD5251037, 0xAFA448F1, 0x7DAFC95A, 0x1EA69C3F,
        0xA417ABE7, 0x5890E423, 0xB0CB70C0, 0xC85025F7, 0x244D97E3, 0x1FF3595F, 0xC4EC6396, 0x59181E17,
        0xE635B477, 0x354E7DBF, 0x796F7753, 0x66EB52CC, 0x77C3F995, 0x32E3A927, 0x80CCAED6, 0x4E2BE89D,
        0x375BBD28, 0xAD1A3D05, 0x2B1B42B3, 0x16C44C71, 0x4D54BFA8, 0xE57DDC7A, 0xEC6D8144, 0x5A71046B,
        0xD8229650, 0x87FC8F24, 0xCBC60E09, 0xB6390366, 0xD9F76092, 0xD393A70B, 0x1D31A08A, 0x9CD971C9,
        0x5C1EF445, 0x86FAB694, 0xFDB44165, 0x8EAAFCBE, 0x4BCAC6EB, 0xFB7A94E5, 0x5789D04E, 0xFA13CF35,
        0x236B8DA9, 0x4133F000, 0x6224261C, 0xF412F23B, 0xE75E56A4, 0x30022116, 0xBAF17F1F, 0xD09872F9,
        0xC1A3699C, 0xF1E802AA, 0x0DD145DC, 0x4FDCE093, 0x8D8412F0, 0x6CD0F376, 0x3DE6B73D, 0x84BA737F,
        0xB43A30F2, 0x44569F69, 0x00E4EACA, 0xB58DE3B0, 0x959113C8, 0xD62EFEE9, 0x90861F83, 0xCED69874,
        0x2F793CEE, 0xE8571C30, 0x483665D1, 0xAB07B031, 0x914C844F, 0x15BF3BE8, 0x2C3F2A9A, 0x9EB95FD4,
        0x92E7472D, 0x2297CC5B, 0xEE5F2782, 0x5377B562, 0xDB8EBBCF, 0xF961DEDD, 0xC59B5C60, 0x1BD3910D,
        0x26D206AD, 0xB28514D8, 0x5ECF6B52, 0x7FEA78BB, 0x504879AC, 0xED34A884, 0x36E51D3C, 0x1753741D,
        0x8C47CAED, 0x9D0A40EF, 0x3145E221, 0xDA27EB70, 0xDF730BA3, 0x183C8789, 0x739AC0A6, 0x9A58DFC6,
        0x54B134C1, 0xAC3E242E, 0xCC493902, 0x7B2DDA99, 0x8F15BC01, 0x29FD38C7, 0x27D5318F, 0x604AAFF5,
        0xF29C6818, 0xC38AA2EC, 0x1019D4C3, 0xA8FB936E, 0x20ED7B39, 0x0B686119, 0x89A0906F, 0x1CC7829E,
        0x9952EF4B, 0x850E9E8C, 0xCD063A90, 0x67002F8E, 0xCFAC8CB7, 0xEAA24B11, 0x988B4E6C, 0x46F066DF,
        0xCA7EEC08, 0xC7BBA664, 0x831D17BD, 0x63F575E6, 0x9764350E, 0x47870D42, 0x026CA4A2, 0x8167D587,
        0x61B6ADAB, 0xAA6564D2, 0x70DA237B, 0x25E1C74A, 0xA1C901A0, 0x0EB0A5DA, 0x7670F741, 0x51C05AEA,
        0x933DFA32, 0x0759FF1A, 0x56010AB8, 0x5FDECB78, 0x3F32EDF8, 0xAEBEDBB9, 0x39F8326D, 0xD20858C5,
        0x9B638BE4, 0xA572C80A, 0x28E0A19F, 0x432099FC, 0x3A37C3CD, 0xBF95C585, 0xB392C12A, 0x6AA707D7,
        0x52F66A61, 0x12D483B1, 0x96435B5E, 0x3E75802B, 0x3BA52B33, 0xA99F51A5, 0xBDA1E157, 0x78C2E70C,
        0xFCAE7CE0, 0xD1602267, 0x2AFFAC4D, 0x4A510947, 0x0AB2B83A, 0x7A04E579, 0x340DFD80, 0xB916E922,
        0xE29D5E9B, 0xF5624AF4, 0x4CA9D9AF, 0x6BBD2CFE, 0xE3B7F620, 0xC2746E07, 0x5B42B9B6, 0xA06919BC,
        0xF0F2C40F, 0x72217AB5, 0x14C19DF3, 0xF3802DAE, 0xE094BEB4, 0xA2101AFF, 0x0529575D, 0x55CDB27C,
        0xA33BDDB2, 0x6528B37D, 0x740C05DB, 0xE96A62C4, 0x40782846, 0x6D30D706, 0xBBF48E2C, 0xBCE2D3DE,
        0x049E37FA, 0x01B5E634, 0x2D886D8D, 0x7E5A2E7E, 0xD7412013, 0x06E90F97, 0xE45D3EBA, 0xB8AD3386,
        0x13051B25, 0x0C035354, 0x71C89B75, 0xC638FBD0, 0x197F11A1, 0xEF0F08FB, 0xF8448651, 0x38409563,
        0x452F4443, 0x5D464D55, 0x03D8764C, 0xB1B8D638, 0xA70BBA2F, 0x94B3D210, 0xEB6692A7, 0xD409C2D9,
        0x68838526, 0xA6DB8A15, 0x751F6C98, 0xDE769A88, 0xC9EE4668, 0x1A82A373, 0x0896AA49, 0x42233681,
        0xF62C55CB, 0x9F1C5404, 0xF74FB15C, 0xC06E4312, 0x6FFE5D72, 0x8AA8678B, 0x337CD129, 0x8211CEFD,
    ],
    [
        0x61B0B02F, 0x00E27716, 0xBF32D884, 0x6FA356FF, 0x35842720, 0x54607261, 0x7828C5AE, 0x294211CF,
        0x4E81528B, 0xDD5457A7, 0x0D9D32BE, 0xAF55B23F, 0x3F8699A0, 0xDBB4AF42, 0xD744DC65, 0x0C93ECF0,
        0xE359680B, 0x046DF2EF, 0x1BF24487, 0x595146D2, 0x8BDFD42B, 0x2B0D38EA, 0xAC18A09F, 0x73AF8D78,
        0x68AEBA06, 0xC5FFA500, 0x8DB36B2D, 0xA040D9B7, 0x8583C012, 0xB5FC22E3, 0x239714D5, 0xA795C69A,
        0xB43FBCDB, 0x628D4AE0, 0x187A5941, 0xA9491C34, 0x77CB9482, 0x14530C67, 0x478A1253, 0x754AE323,
        0x7EA8C1E7, 0x9087BFAF, 0xD219BBE5, 0x608500CB, 0x3E6940A4, 0x3B7D5F5B, 0xB95E86F7, 0x08CDC2E1,
        0x02F7AD77, 0x40B5DAF1, 0x8E725492, 0x740FA82C, 0x3094F8E8, 0xC925810A, 0x89FA96C6, 0x7C4375D1,
        0x2F36B383, 0xA461C74F, 0x4426906D, 0x20093EDA, 0x2C41DFD8, 0xD8E06097, 0xD08B1A03, 0x5EBBEA72,
        0xAD560825, 0x795B1388, 0x7D6F4DFE, 0xE7D9F74E, 0xEC8919A1, 0x82F0B55F, 0x0B70FCD4, 0xC433D7C7,
        0x0305C3B8, 0x9CCC826E, 0x9B0A5848, 0xB3A47130, 0x633D24ED, 0x3DDCE217, 0xB8376E76, 0x0139FDAC,
        0x5CA23769, 0x6BBE5B59, 0x883BAEBB, 0x21D6E605, 0x53B623CD, 0xF5F1CB80, 0x4ACF04C2, 0x4C3A91B4,
        0xDA45E998, 0xB15F7B24, 0x57A74CBC, 0x674E0B1D, 0xB0D18A3D, 0xE9D0677B, 0x382F9DC0, 0x34031701,
        0x1A9B1B02, 0xE5DE7DA9, 0x33C4A173, 0x4D1B8B0F, 0x376E2F6F, 0x247E2EEE, 0x27F6CFA8, 0x2814E04D,
        0x155AE77E, 0x2592483C, 0x17473143, 0x9923CD46, 0xDF1A06D9, 0x724F69E6, 0xB76B70FA, 0xB6A536FB,
        0xF4EE0951, 0xEE357EEC, 0x874DB952, 0x52579C1F, 0xFEE40F32, 0x5D4B3009, 0xBC71EF8A, 0xFDAC884B,
        0x4B9C50CC, 0xF72BB88E, 0x7B0B974C, 0xABD3CC8C, 0x58C961C5, 0x2D734228, 0x5AFB05BF, 0xAA766227,
        0x76E8BDF9, 0xC70E291E, 0xFB48189D, 0xCAF40A79, 0x0F298C9E, 0x9F1CF3D3, 0x658E7470, 0xC2CE3B26,
        0x6D04D3DF, 0x8CC7808D, 0x92BD43C9, 0xA88CB490, 0x5B52840D, 0x32D8FF58, 0xD9B27FC8, 0x0ED22C15,
        0x7A636F5A, 0x56999E18, 0xF050DBF2, 0x42675129, 0xA23C2A1A, 0x98669B19, 0x1E881540, 0xD3F589F3,
        0xD164F55C, 0x13CAD545, 0xF3AAF0AB, 0x5FA1D0B6, 0x9AEC4908, 0xA5E53AA2, 0xE212A254, 0x9D6CF60E,
        0x2E901E6B, 0x12796C36, 0xC8C283AD, 0x411D2163, 0x07D7E435, 0x4611DE74, 0xA6965A93, 0xE4342660,
        0x26C3E57F, 0xF11095F5, 0x93A98F91, 0xBA2EB74A, 0xC365EE04, 0x5538A7E9, 0x1D75DD3E, 0xCC3153E4,
        0xBB77E821, 0x91B70E44, 0x0691D65E, 0xDE165CA6, 0xA378C968, 0xCD1334D0, 0xCE006694, 0x710C283A,
        0xE62DC87A, 0x1C1EF97D, 0xE0AB92AA, 0xB246792E, 0x4FB9FADE, 0x5174AC1C, 0x69682557, 0xE8985537,
        0x45A66DA3, 0x961F4B99, 0xDC7F3CF8, 0x4902020C, 0x6E17FB7C, 0xC0FD8747, 0xCB8FEB6A, 0x8458CEB9,
        0x64BCF196, 0x1021AAD6, 0x50C01FB3, 0xAEC5D175, 0x864C9A22, 0x7FE3851B, 0x3CB8AB33, 0x319A4EFD,
        0xEBC66513, 0xE1E9E164, 0x48B13585, 0x8FDDA3E2, 0x36D41D07, 0x70E19F5D, 0xC1273F39, 0x836A98B1,
        0xA1303371, 0x3A2C7881, 0x0A5D1686, 0xD5060150, 0x05C8B68F, 0xBEF8A6C1, 0x2A820311, 0x80BA4F10,
        0xEA9F76CA, 0xEF80CA3B, 0xD47C4755, 0xBD07ED89, 0xFAC17A95, 0x399E2B56, 0x16DAD26C, 0xCF2A41A5,
        0x6AADB1EB, 0x81DB5EF6, 0x6CE62D9B, 0x9EEF07FC, 0x666210BD, 0x94202049, 0xF95C3962, 0x19A0F4B0,
        0xF2F963B2, 0x97EB7314, 0x43086466, 0x1FED0DCE, 0xF83EFEDC, 0xC6E7A431, 0x8ABF8E38, 0x22F345B5,
        0x957B5DDD, 0xFC1593BA, 0x1101A9C3, 0xF622BE2A, 0xEDFE7CC4, 0x09EA3D9C, 0xFF24C4D7, 0xD6D56AF4,
    ],
    [
        0x487600CE, 0x425C8FFA, 0xBEC67996, 0xD0CC610C, 0xB2A1D01D, 0xADAE8C7A, 0x0AB5D392, 0x020B2E45,
        0x30325588, 0x8B630249, 0x927320E4, 0x2E98A92D, 0xB70817DF, 0xEB6858AA, 0x203186A6, 0x225D0823,
        0x3F66BABE, 0x7E4853BF, 0x6E96684E, 0xE63BD63D, 0xD46EC4F8, 0x4B2E89A7, 0x0CA5AD9D, 0xF0C39E2E,
        0x6D866DFB, 0x1927FE8A, 0xA4DB62D2, 0xF4C06E25, 0x8A1DB2F9, 0xAB7E0F9E, 0xFBCB5A79, 0x132B6A2A,
        0x78344DA3, 0x08077B50, 0xA378DA3F, 0xB0E5A681, 0x94EF414F, 0xAF8894C2, 0x52374B69, 0x45173E46,
        0x6AA66044, 0x2FBF64FC, 0x9185FFC3, 0xBC8C07E2, 0xDC11196F, 0xC2DE9B41, 0x76F006B9, 0xDB393172,
        0x679750DB, 0xCA655204, 0x79B1AA01, 0x6B7F1DB1, 0xAA834C35, 0x9B121507, 0x6959335A, 0xB66FC3D5,
        0x1F7D56ED, 0xF274F294, 0x5D491602, 0x77B2DBE8, 0x3E92EF61, 0xE0D5DDA0, 0x14EEC07F, 0xBB0C3B3E,
        0xBF9A46B8, 0xEE513ACF, 0xC577F6BC, 0xD162DFD9, 0x0795B718, 0xEC1A3895, 0x68A81EB7, 0x7C3F3C47,
        0x9D1FEC76, 0xC3B61132, 0xA733BDA9, 0x983AD434, 0x93D799BB, 0x9ED26670, 0x00FADC1C, 0x56BE4843,
        0x094CA491, 0x6FF2B9C4, 0xA293C933, 0x2D4228EB, 0x1EF4BB77, 0x069BB65C, 0xA9A02CDA, 0x8F1691D4,
        0xB44F0E5E, 0x8CE7A52B, 0x9F61E45F, 0x492DEE16, 0xD9D927C5, 0xDA711A09, 0x47A92AC0, 0xA5227215,
        0x1B10011A, 0xFAEA5F7D, 0x54195DE0, 0x90CE638D, 0xC4F798EA, 0x81D62F38, 0x1D14D521, 0xAE231465,
        0x38D3E126, 0x353EA748, 0xE1C875D3, 0x7BBBB4E7, 0x0FFBE50E, 0xEF289ABA, 0xBA997F7C, 0x50C2D887,
        0xC95B909A, 0x6CB9FCF0, 0xDDE9D158, 0x62ED7156, 0x04550467, 0xEA3D807B, 0xE56AE7AD, 0xFF571C54,
        0xE4C1D2B3, 0x152FA2FF, 0x2101A3F3, 0x7A26F9CC, 0xCFC91280, 0x2C67CBCA, 0xFC243224, 0xFE2A78D8,
        0xB86937A8, 0x74A2F0A2, 0x99470D8B, 0x18E2C8C6, 0xF7607E0B, 0xF6ADBC85, 0x58C54E74, 0xCBF1C214,
        0x0E8FB14A, 0xC0B84500, 0xC8A75462, 0x645FCF5D, 0x4AB48466, 0xD6A3E3FE, 0x95F57A20, 0x4C4DB0A1,
        0x430DC782, 0x85A444BD, 0x885E7DE9, 0xAC3CAFEC, 0x634B0A39, 0xC1EC3903, 0xD58AE2AB, 0x4FF65B71,
        0xB381952F, 0x175347F6, 0xE7523F97, 0xE9F97C89, 0xDF9413DD, 0x72B3692C, 0x9740CA84, 0x80D170F7,
        0x0B4E3012, 0xA056B39C, 0xCC151BE1, 0x37E6CC60, 0xE29D6F52, 0x0DBC8D3C, 0x3C1B188E, 0x39CA23AE,
        0xD705B831, 0x89DCEA36, 0xA8F37763, 0x4D4A51EF, 0x5E02FDF2, 0x5F09FAFD, 0x36AA356C, 0x719EE617,
        0x5AE19F1E, 0x3DDF4973, 0x4EB0AC83, 0x7F3597F4, 0x318EA153, 0x32D0F8A5, 0x16469319, 0xFDAB74CD,
        0x1CFE8340, 0x26891F59, 0x517A87EE, 0x668740DE, 0x44FDAE4C, 0x55FFC61B, 0x70F88E90, 0xA103ED29,
        0xB18B9DE6, 0xB9AF26C8, 0x128459F1, 0xCD29BF27, 0x4138039B, 0xF5ACAB05, 0x404443CB, 0xF882A010,
        0x7572736A, 0x46508811, 0xD270214D, 0x61E40B55, 0x23905ED6, 0x60210C22, 0x290A8568, 0xD8C75CC9,
        0xB591346D, 0x591EB5E5, 0x10252DAF, 0x96EB65DC, 0xA61C3699, 0x83186728, 0x11417664, 0xDEDAD7AC,
        0x337B9CB0, 0x87BA2B8F, 0x735AF375, 0xC66BE857, 0xE3DD296B, 0x3445C14B, 0xC70E3D7E, 0x24FCE03B,
        0x86E8EB08, 0x25CFFB93, 0xCED48A9F, 0xD36DF5B4, 0x3AD810C1, 0x570F82D0, 0x8EE3D9C7, 0xBD6CCD8C,
        0x2B20DE98, 0xE8134AE3, 0x288042B2, 0x2AB7C530, 0x1A549237, 0xF3438106, 0x0130BE6E, 0xF9004F5B,
        0x5BBDF7D7, 0x03588B0D, 0xF12C05B5, 0x8DCDA842, 0x53360913, 0x9A64F178, 0x27066C51, 0x050457B6,
        0x9CE0E91F, 0x5C759686, 0x659CCE0F, 0x827C240A, 0x3BC4253A, 0xED8DF4D1, 0x7D7922A4, 0x849F6BF5,
    ],
    [
        0x3A13DB47, 0x0FA73FED, 0xF59774B2, 0xA82D2E39, 0x1B01C668, 0xBA41E59E, 0x696D3AEE, 0x973F5F48,
        0xE1E9E028, 0x90237B57, 0x6467E6C7, 0xE080FBA8, 0x3C771A13, 0xBF9DF688, 0x2C3EB876, 0xE4EAC142,
        0xD8240C0F, 0x31CEFD5C, 0x8BF376DA, 0xCDEC51AB, 0x4D4919C6, 0xC35F2904, 0xEDBFEB08, 0xDD7C0A6F,
        0x74D33B98, 0xD7D5B0C0, 0xE30084FD, 0xB861A6D5, 0x3BCC8C91, 0xBBB717A6, 0x575C5D74, 0xF1DDF1A4,
        0x4B3D5C64, 0x1508DDBB, 0x76ED5317, 0x52E0C463, 0x10144197, 0xEB5BA202, 0x4160B1F0, 0xBC946A7C,
        0xAC4B70D8, 0x4AB4A424, 0x9B6AC0AC, 0x35DCD9A5, 0xAA302BC9, 0xD6EBFEEB, 0x065EEAB7, 0x55B99035,
        0x683A010E, 0x421F10D0, 0x21C6A980, 0xC86378C1, 0x7DEEB734, 0xB1C8301F, 0xC52F2D2C, 0x862BFF7D,
        0xA9629441, 0xA3D97F59, 0x1718BD01, 0xC6835582, 0xB0FE00FF, 0x190C9F73, 0x5BD756EC, 0x8847F2D4,
        0x11C4DF51, 0xB288068C, 0xAE2E28B3, 0x56B63610, 0x5A123EBA, 0x6E0F8906, 0x03BC6649, 0x28093C14,
        0x7E488685, 0x4338E49F, 0xFBE71358, 0xD571E30C, 0x081612F1, 0x820AC972, 0x9999228F, 0xA633DE9A,
        0xC7D2464C, 0x845273BF, 0x7B3616DB, 0x1FAF02AA, 0xB99CA0B4, 0xD1D4F7D9, 0xE7A3D060, 0x651B50F2,
        0x7272AA69, 0xB3DA9753, 0xEFE40D1E, 0x9443779D, 0x33FA8F1A, 0x47BA8EDD, 0xF7899965, 0x3F5557C2,
        0xC99E3526, 0x44AAD554, 0x1E10F3D6, 0xEE9A0BB6, 0x8D799DD2, 0xB5ACCF7E, 0x9F215E05, 0xD0542A5F,
        0xF37DD6FE, 0x66916C36, 0x045D1E4A, 0x9C1EEF1B, 0x37577120, 0x803CCB19, 0x96CD593A, 0xF968A7CE,
        0x22CB60EA, 0xEC7B6803, 0x26A41855, 0xD2A5CA15, 0xF4042FA2, 0x1806CD87, 0x9EABBEB1, 0x584095FC,
        0x2AB84071, 0x38EFF83F, 0x61A1C812, 0x142A61C5, 0xFFA80F8A, 0x45118A9C, 0x29657262, 0xFDE62786,
        0x50F8A50A, 0xD94F7CA1, 0xCA02E8C4, 0xF06FE9F5, 0x5FE81C0B, 0x858A5277, 0xB4E34DA7, 0xE9CFE7CA,
        0x8AFCCCFA, 0x8FE17E50, 0xA7BDB97A, 0x530BC7DE, 0x818C67E2, 0xA2D8442D, 0x36461D93, 0x91F6982A,
        0x01933D2B, 0x2D51BF38, 0xEA87B678, 0x398B7909, 0x5C2C0366, 0xCBAE31FB, 0x6A19343D, 0xFC1A42DF,
        0x7856AF37, 0x7FFFACCC, 0x635026D1, 0x5D84FA46, 0xE2590ECD, 0x62F2F423, 0xB6BBBC32, 0x9D8F4C96,
        0xC464374E, 0x4E69838D, 0x5E9BBB94, 0x02C1435A, 0xBEE52190, 0xB7DE246C, 0x40FB6D99, 0x6FADD84B,
        0x3495E143, 0x6CB31B07, 0xCE255B5E, 0x798E49C3, 0x321D8B8E, 0x3D53C3E7, 0xD303D3E4, 0xDC0D936A,
        0x30F56FDC, 0xC0A24ED7, 0x499809B9, 0x2774B4B5, 0xA1E29EE6, 0xA007DCE0, 0x0E314AAD, 0x1D82E21C,
        0x984E9B2F, 0xE87AAD25, 0x6D17EC2E, 0xAFF1116D, 0xC258CEA3, 0x2B45A161, 0x87FD45F9, 0xC1906944,
        0x2EB1D275, 0x4CA0A392, 0x1CC2FC29, 0x6B8D1F6E, 0x4F4D7AC8, 0xDF5AF9E1, 0x093996F8, 0xDA9F87B0,
        0xE6BE80E9, 0x73783340, 0x162665EF, 0x5428F545, 0x71CAB55D, 0xAD6B4B52, 0xF632B3E5, 0xD43BED3C,
        0x92F9C2AE, 0xA57F6B1D, 0x0A056E84, 0x20F7634D, 0x7CC7B230, 0x05359A33, 0x89761522, 0x12D1644F,
        0xCC27A883, 0x48B08D18, 0x131CD431, 0x1A4CD789, 0x0D705ABC, 0x25B23879, 0xE5F47D56, 0x246CBA27,
        0x678182F7, 0x4644AB3B, 0x7A157595, 0x0729540D, 0x23A985D3, 0x5166C55B, 0x00854F6B, 0x0B86DABD,
        0x75F00711, 0xF2DFD1B8, 0xBDC5EEF4, 0x8EB5929B, 0x0C9608AF, 0xDE7525CB, 0xFE3747E8, 0xABDB587F,
        0x9AD048F3, 0xF842043E, 0x8C732070, 0x2F2291A9, 0xCFD60516, 0xFA34818B, 0x772014A0, 0x3E6E3200,
        0x83A662E3, 0x707E9C81, 0x600E2C7B, 0xA44A88BE, 0x59C3F0F6, 0x95C92321, 0x939239CF, 0xDBC0AE67,
    ],
    [
        0x7F19B458, 0xE0C3EBFB, 0x6D3705F2, 0x2F95D838, 0x5E6E1A99, 0xA1555BA3, 0x35ED5DB1, 0xE8B890EC,
        0x3E2E0767, 0x1606476F, 0x848FE1AA, 0x8D0EA0C7, 0xF8298704, 0xFAE6BCBD, 0x97E159D8, 0x82EFB64C,
        0xB0D076AF, 0x20724D94, 0x6B272980, 0x6F168F44, 0x24D63BD5, 0x6A3CA1A4, 0x3F4C8917, 0xB2A13556,
        0xEF26CAC8, 0xEC02845F, 0xE6FEE650, 0x4E77387C, 0x142F85FC, 0xB16F3DC4, 0x54FCC6D6, 0x78B0A702,
        0x4548D6F5, 0x0A694BAD, 0x2BA21BE4, 0x680AE09B, 0x1E3AB1F8, 0x6E366CE6, 0x9F8D324F, 0x9B5E8C89,
        0x395C06F0, 0xBB53DA09, 0xE763D196, 0xDA6A0AF1, 0x0870E477, 0xCB405E22, 0xEB44B890, 0xD13E7442,
        0x03656BD0, 0xC23B1E23, 0xD9DD8BDB, 0x43750EB7, 0x0B7340EE, 0xACA44A07, 0x1DE2A6CA, 0x2AEC4E0E,
        0xA52B4927, 0x615A7A72, 0xCD6201CF, 0xCEFFB3A8, 0x8EC7E735, 0x918E4254, 0xEE9F128C, 0x882008EA,
        0xE21FF474, 0x0DE5BEF6, 0x8FC4ABD7, 0xA7DB5830, 0x87C60D18, 0x7E9B0B4A, 0xB3AF3775, 0x8BD3730F,
        0xD6B37088, 0x9A7B9655, 0xF2A830C1, 0x86964161, 0xD7ADFD3C, 0x23355C73, 0x94C1C25B, 0x1ABA5ADA,
        0xD0F17D06, 0x9CF88081, 0x2E077586, 0xA91B036C, 0x119E7119, 0x80B90945, 0xC3D2B09D, 0xB5A0DD66,
        0xE1C9FC1B, 0x3094A484, 0x2688EA8E, 0x92A763C0, 0xA62CF637, 0x2D5697EB, 0x5C66025E, 0x17F4672C,
        0x25BBED11, 0x369152E8, 0xCC4E3FD4, 0xDDDED33D, 0xB4C0C34E, 0x44906D93, 0x50CF2DD2, 0x311C7EA6,
        0x6728EE1E, 0x60E957CC, 0x37B4A346, 0xED09D53F, 0x4014B9AC, 0xAE41D047, 0x63112CBC, 0xF146B700,
        0x66F29B2B, 0x6C85AE6E, 0xAB0478ED, 0x526B3EA0, 0x7B7CC0FE, 0x004FB260, 0xFECEBD34, 0xF959FBB8,
        0xB947101F, 0x8CC239BA, 0xBA74158F, 0xF31E6936, 0xDCF53152, 0xE9DAC810, 0xF023D4CB, 0x3D30DBCD,
        0x997E4FFA, 0xB8C5F382, 0xBF08E9EF, 0xE40B942F, 0x74BCDC97, 0xFF9979CE, 0x3CEBF179, 0x29A56068,
        0xA2E46812, 0x2C5B2EBE, 0xFC867239, 0x1952AD71, 0x90B71C6D, 0xC6CDAC03, 0xC539BFA2, 0xF66020A5,
        0xC84A647B, 0x69DC1691, 0x5951191D, 0xD4386670, 0x8576AF41, 0xE34D88A9, 0x72E7A87E, 0xD33192C6,
        0x286C560D, 0x5D811F51, 0x0542FE85, 0xC0B62321, 0x38A3817F, 0x5B0F279C, 0x898C62B4, 0xA3176F2E,
        0x34AA9595, 0xE51DD29A, 0x21D5B5F4, 0xF5F324F7, 0x4880C4B2, 0x9D57A54B, 0xB600D7D3, 0xDFF6E29E,
        0x1F9336F3, 0xAD7AD9B0, 0x753F340B, 0xA07F3CE9, 0x554B8313, 0xC7B12A3E, 0x81F7E332, 0x0F124429,
        0x7D250CB3, 0x96670F8A, 0x766133A1, 0x8AAB9D8B, 0xCA8AF06B, 0xDB13CCFF, 0xAF97E8DE, 0x41101DF9,
        0x4B019125, 0x71DFF81A, 0x182DDE87, 0x4245F7DF, 0xDEEE7F31, 0x4FBDFA16, 0x019A5020, 0x9354464D,
        0x151854E3, 0xFB649A62, 0x1CB22805, 0xBE848A83, 0x3B49CD76, 0x770DAA92, 0x732ABB24, 0xFDD19E98,
        0xD2E80043, 0x4789A92D, 0x58587BC9, 0x490C3A78, 0x7C9D453A, 0x7998BA57, 0xA4B56A7D, 0x95E39FB9,
        0x27AEC7D9, 0x98874CDC, 0x53AC7C59, 0x6405438D, 0xC4242149, 0x126D2226, 0x1B71CBC2, 0x338B86B6,
        0xC992F9FD, 0x4CFBF564, 0xBC9C8D5A, 0x627D5FBB, 0xD53D2B14, 0x5F6898B5, 0x2221250A, 0xF4D965E1,
        0x3AE048E0, 0xC1BF6E9F, 0x02A99C2A, 0x4DF9827A, 0x0CF014E7, 0x13D7180C, 0x57322F63, 0x4650FFAB,
        0x0EFDC5E2, 0x061A13D1, 0x07FA55DD, 0xF7CCC1AE, 0x7A03EC48, 0x70781128, 0xCFCA9340, 0xBD345153,
        0x9E838EBF, 0x6522613B, 0x565F5333, 0x1015CEC5, 0x4A79EFC3, 0x5AA6A25D, 0x09822615, 0xD8D87765,
        0xB75D9908, 0xA8EADF5C, 0x51331769, 0xEACBCFA7, 0x04BEF26A, 0x32C80401, 0xAAD4C9E5, 0x8343E51C,
    ],
    [
        0xB98FD895, 0xBD668A92, 0xB89ABB2E, 0xFA0A5642, 0xDE5B9B33, 0x1E376359, 0xF33AFD57, 0xA71EB7F9,
        0x91AA4213, 0xE7CE2415, 0xD0A3670D, 0xCB80A1AE, 0xC43C6E9A, 0x34527F29, 0x9A9FDA8A, 0x1B88A685,
        0x0CF9E49D, 0xE26D6AA6, 0x1F4E4CEB, 0xA0903CC1, 0x7CCC43E7, 0x46200708, 0x76082BB6, 0xDAF51132,
        0x7E26B08E, 0x21B5EE04, 0x3967D13E, 0x9DD846DC, 0x3717ACD9, 0x8A937A2C, 0x841F9452, 0x4B35146D,
        0x5EF1EB70, 0x3B6B8490, 0x78A1BDBC, 0x1DAE9AB8, 0x075EA424, 0x2A423DFC, 0x7003B181, 0x9694D7B1,
        0x949BF531, 0xE64D2745, 0xB591C6C2, 0x0989C23B, 0x25ADB2DE, 0xFD1CA88B, 0xCF50374D, 0xD8166830,
        0x52841F00, 0x3EB199DA, 0xFC8C1E26, 0xAD7AAFBA, 0xF938CCA7, 0x2912D5C0, 0x11253A79, 0x28F393ED,
        0x267B10F8, 0xF406012A, 0xEA0F60F5, 0x43A83F20, 0x0232821D, 0x83EA9893, 0x352A890C, 0xE8DA5734,
        0x7A295DE6, 0x44EE6C0F, 0x7D63F1F1, 0x5A4C3E62, 0xCE925036, 0x81F7CF09, 0x54DE17D4, 0x4DFD0D63,
        0x03FB2022, 0x73C19676, 0x8E414782, 0x3D5A8C53, 0xE3CD09A1, 0x042E2EFD, 0x19570EB0, 0xC3E4FBEE,
        0xAB148384, 0xB2BC1205, 0x4E5C778F, 0x5B97DFF2, 0xE4779DFB, 0xFB59A255, 0x0F769E69, 0x41624950,
        0xF810E1D3, 0x851519D7, 0x2F54B97E, 0x93E7855E, 0x599DAD4C, 0x2D58F07F, 0xD1CA26A0, 0x0D2BC9EF,
        0x458E36A5, 0x68409CB3, 0x6F7EE7A2, 0xF6CFB3A8, 0x0EDFF3A4, 0x2CC372CE, 0x9F69DB49, 0x63A0E87D,
        0x7B5DB888, 0xC5477171, 0x36055F60, 0xA6E51516, 0x3171FF98, 0x12F44DC8, 0xCAD7751F, 0xDFACB6CD,
        0x7F310AB7, 0xD56C38E3, 0x66D041C5, 0x6A180BF0, 0x0833FAEA, 0x47EF1A6F, 0x16002174, 0xA8E15C77,
        0xF52F30CA, 0xD621E99F, 0xE13F51B9, 0x8BF67DF7, 0x487D9510, 0x4298ECBD, 0x01DDA7FF, 0xBA3E083C,
        0xDD3D32D8, 0xE5B6D61A, 0x1CDCD2E4, 0x50D2D975, 0x53FFAAF6, 0xAF687BB4, 0x6595293A, 0x5160C7DD,
        0x5DF286AB, 0xD2A297C9, 0x13D5BAE1, 0x156F7007, 0x0A1B28BB, 0x88B04F9C, 0xDC274AE9, 0x234964E8,
        0x40A92D17, 0x6C9CB561, 0x5CE68106, 0x0BFE4037, 0xBFB78B4B, 0x67CBDE41, 0xB0012519, 0xC17804D1,
        0xEB451C97, 0x69B2FC28, 0x33E8556A, 0xCD099265, 0x9579C49B, 0xE9C48ECB, 0xBB4A9F8D, 0xB16EEA73,
        0xD773F958, 0x6011D33F, 0x9E87A354, 0x182CB486, 0x98225296, 0xA46AE5FA, 0x3C618D5F, 0xBC815340,
        0x3AD4BF66, 0xEC707EE0, 0x62347C1B, 0x566406C7, 0xC0AB5A51, 0x1A1ADC18, 0xAEC945A9, 0x10D1915B,
        0x6D23CB0E, 0xA5FCCEB5, 0xFFBE4899, 0xFEBBDD1C, 0xB60E61EC, 0x279E447B, 0x570BA0BF, 0x77078778,
        0x6BC01638, 0x4C4B1802, 0xF0A48087, 0x8C3BE60A, 0xD3E25467, 0x55741D0B, 0x714FC59E, 0x4A0CE2AF,
        0x9B8D35DF, 0x49D33143, 0x38BD7603, 0x6EEDF794, 0x24485823, 0x89D9884F, 0x20F0628C, 0x82F8ABAA,
        0xDB28D056, 0xEF191BE2, 0xEDC82F4E, 0xF2EB2AD5, 0x9CD60C39, 0xAA55595C, 0xBE86BE12, 0xA9BFF272,
        0xE0A5FE5A, 0x5F824B46, 0xC256C114, 0xF753786C, 0x3013D4FE, 0x79A7652B, 0x327FF64A, 0xC7C5E07A,
        0x99C64E68, 0x2265A92D, 0x2E7C6BC3, 0x61E90247, 0x97E08FCC, 0x80C774D6, 0xB436A5F3, 0x8FC239A3,
        0xAC46F825, 0x06DB79C4, 0x758305D0, 0xF1A6E37C, 0xB799BCB2, 0xD4305E6E, 0x90B83B11, 0xC60266DB,
        0x92AFCA91, 0x648AC06B, 0xCC516948, 0xA14323F4, 0x58447321, 0x3F0D5B64, 0x7204CD83, 0xD9721389,
        0xC9B42CCF, 0xA375EF80, 0xA2EC6D35, 0x17BAC32F, 0x87E303E5, 0x148534BE, 0x00B9AE27, 0x4F1D903D,
        0xEE39F45D, 0x052DEDD2, 0x745F6F44, 0x86FAC801, 0x8DB322AC, 0xB3240FC6, 0x2B9633AD, 0xC88B001E,
    ],
    [
        0xD93B928F, 0x15FCCA5F, 0x1FEEC53E, 0x780A03EB, 0xC2EA8AD0, 0x5465EE0D, 0x483FEDAA, 0x9DAF59F1,
        0xB877B015, 0x595C8F9B, 0x7CB671DB, 0xEB800ECB, 0x0421C47A, 0x02B97B8C, 0xBAB4D553, 0xADC745BA,
        0x7DDAF8B1, 0xD5CFB16C, 0x5338AF82, 0xD0478D81, 0x8D9B344D, 0x44074BC5, 0x4CC51188, 0x000F6DA7,
        0xBBE44DD7, 0x9C4BD055, 0xB062B296, 0x5D416BAC, 0x9334EBBF, 0x8A9FA94F, 0xD6255C6A, 0x7BF588E4,
        0xA64E533C, 0xB958FAF6, 0x56D51E9D, 0x5275E669, 0x87E6A8A2, 0x5CC01061, 0xBFF22B60, 0xC811BAC4,
        0xAC1A6832, 0xA1B3D459, 0xE9C2138E, 0x1B18EC64, 0xC6FD1422, 0xDA989842, 0xFD303658, 0xF7DD9FA0,
        0xC3932695, 0x9F81ABAE, 0x603962C0, 0x64166949, 0xA0370B18, 0x4FF438D2, 0x996D1F00, 0x3D64DB4C,
        0x1E675AD6, 0xCFD01D47, 0x901E3F57, 0xC9A541E9, 0x92088213, 0x756FFF3A, 0x21510AB8, 0x8357A4B9,
        0x17F3DE8B, 0x34712730, 0xDEBCE78A, 0xBE2D5E20, 0xCEF7C039, 0x97FBF79F, 0x0BF96197, 0x86824768,
        0xAEF8350B, 0x2988E1EF, 0x43F02D34, 0x4B3E8E78, 0xD74A676D, 0x7F76F0BE, 0x2FD31CFD, 0x7073D97C,
        0x011F000F, 0x6E9AB3C6, 0xB66B7A09, 0x4D1D17AF, 0x57BF312D, 0x72A277FF, 0x4229568D, 0x5F50EA26,
        0x1CB0E854, 0xEA95E9BB, 0x2DEFE340, 0x207BB41B, 0x25CAFC2E, 0x14C4B602, 0xF17906BD, 0x3B52A135,
        0x0A89A094, 0xECB77523, 0xF6C8A648, 0x6F708BB4, 0x3CFE1AE1, 0x05361680, 0x58D23767, 0x396A7373,
        0x504515CF, 0x802A40A4, 0x45409CD8, 0x18E7707D, 0x6BBBD2E0, 0xD290095E, 0xB3B22117, 0x66CD843F,
        0x89047FB0, 0xA98F3E71, 0xFAA1D1DE, 0x0D26B96E, 0x5159CC04, 0xF0C3CEFA, 0x3F0E6F14, 0xFC9404C1,
        0xF20395E7, 0x11AB97ED, 0x76C1CD19, 0x2620199E, 0x302B0711, 0x36FFFBCE, 0xCB7D3212, 0x8878A2AB,
        0xAB24579C, 0x388D12DF, 0xDDD89601, 0x63C6AC90, 0x22E1BE05, 0x3EAA054A, 0x9E5483A1, 0x1AD10CD5,
        0x6A1948B5, 0x4A9E6C52, 0xB1A9C843, 0x943120AD, 0x19DBE5FB, 0xAAA7661D, 0xF40624B2, 0xF5AE9056,
        0xCA1C65CA, 0x035B7D46, 0xA72239E8, 0x072E3C29, 0x4E842F75, 0xBCACA303, 0x162C9A4B, 0xBDF644F3,
        0x6C35DC86, 0x2E92F536, 0xEF4F2537, 0x06E86EF9, 0x8F68A5E5, 0xD35A426B, 0x5BF15B50, 0xE33DBD31,
        0xC71BAAB7, 0x77E5D76F, 0x98CB4A91, 0x27EC28F0, 0x9A17D3A6, 0x68A3870E, 0x3515FD77, 0x914D3AC3,
        0x339DE425, 0x84FABCEC, 0xF9995F10, 0x0EA83D27, 0xFBB1897E, 0xDB28552A, 0xC561C3E3, 0xE710C993,
        0x326EDF51, 0x1043D8D1, 0x239C0DA8, 0x2B55BB08, 0x2C0CDD5C, 0x28913B5D, 0x553C0F45, 0xC14464CC,
        0x40AD79A9, 0x4101937F, 0x3A975D87, 0x0C63C144, 0x82EBB5C9, 0x738785F2, 0xD4695466, 0xC0A6C6A5,
        0xB77A5838, 0x7AD92ADA, 0xB4134641, 0x69857862, 0xE88B8CF7, 0x71BD7C33, 0x5E0D9EBC, 0xED668192,
        0x318C02FE, 0xA8A46306, 0xCD0B8070, 0x08B84FF5, 0x4912EFEA, 0x0F324C21, 0x5A235299, 0xC474FEF8,
        0x6DD71B2B, 0xE5CE081F, 0xDC46B72C, 0xE086F1DC, 0x7E4C915A, 0x13DC5072, 0x8133F376, 0xA3D6F4D4,
        0x95DE6A1A, 0xE1429DE2, 0xA427F283, 0x79E2863D, 0x8BD4E007, 0xCC7FB824, 0xF3CC519A, 0xE6DFF984,
        0xB5962274, 0xB27E721C, 0x3709491E, 0x24B5C7B3, 0x9614AE98, 0x6256DACD, 0xA5BAC2C2, 0xF853BFD9,
        0xFF602CDD, 0xD800F665, 0x47EDCF28, 0x9B6C4363, 0x8502CB79, 0xE248A7C7, 0xEE057EE6, 0x655D23F4,
        0x1DBED63B, 0xFE8329B6, 0x8C7C990C, 0xAF499BFC, 0xDF72742F, 0x123A30A3, 0xD12F76EE, 0xE48EAD16,
        0x46A0E20A, 0x618A945B, 0x09E3604E, 0xA2C92ED3, 0x745F4E7B, 0x675E3385, 0x8EE918C8, 0x2AE00189,
    ],
    [
        0xE43BC2FC, 0x1229ED8E, 0x4F743AF7, 0xA1D90A44, 0xD51F3652, 0x6C2B5151, 0x48456E63, 0x608E1EE6,
        0xCB68533F, 0x0DF3FFB6, 0x9806480E, 0xD4FC0B8A, 0x6744FD20, 0x05A41439, 0xAF81F716, 0x6142D23B,
        0x86BEAB77, 0x24804C36, 0x347931F4, 0xF94F39E9, 0xAD0FC8D4, 0xEC12FABD, 0xD80D62FF, 0x78701FFD,
        0x6676D69A, 0x9E8D43A3, 0x13579784, 0x2F954559, 0x58AF1273, 0x1499DD05, 0x1AFAE57C, 0x0F7FA44D,
        0x09CCA09E, 0x30A09955, 0x51FFF0DC, 0xBE94927D, 0x183111BB, 0x4E260EDA, 0x97D78392, 0x32522899,
        0xF47C3BCD, 0xFFE7B89F, 0xE8AB9B7E, 0x6F8A4BCF, 0x2BE5CDA0, 0xD1B1F9A9, 0x7A16C13E, 0xB269DC5B,
        0xB072D90A, 0xC6A5F5E5, 0xDBB9A2F1, 0x7F25698C, 0x82B26702, 0x72EA8FD3, 0xB6DF3C33, 0xBF202C2E,
        0xE5515296, 0xF50081D7, 0x8F3C9E62, 0xC4871CEB, 0xB1BB1372, 0x46C87A23, 0xEB14B204, 0x876F9D74,
        0x420808AD, 0x8D4DFCF2, 0x93F122C0, 0x555BE932, 0x5BB06B4E, 0x4190ACC9, 0xA922754A, 0x10361AB2,
        0xCEED636E, 0x7418C40C, 0xBBDE01FE, 0x11AA09F5, 0x52070491, 0x73B6666A, 0x62CB8690, 0x361920D9,
        0x164CA1A1, 0xFD6CEA08, 0x1D3D823C, 0x3EC96AAB, 0x4A1B7380, 0x6A1A0F67, 0xA05DE7FB, 0x83E876E7,
        0x759B5C8F, 0x3728062A, 0x7ED64630, 0x20B416CC, 0x40D3B6C4, 0x0BBCE834, 0xC7B82454, 0x351C9C4F,
        0x08A1F409, 0xFC7B93D0, 0x31408882, 0xB59FBAAA, 0xF6750349, 0x5CD85BEF, 0xD2AD960F, 0x394BB9E0,
        0x5D9E5693, 0xBDBACFDB, 0x765AF321, 0xEAEEF6B4, 0xAC98A831, 0x2562218D, 0x5FC6405D, 0xE7FDEBD8,
        0xF2B777C5, 0x57B52713, 0x5666C09C, 0x0C2F41B3, 0x3DE115E8, 0x1CCD6C41, 0x68678D1E, 0x5458F271,
        0x8A39E440, 0xBA7AAF24, 0xDE1E711F, 0x69EB4406, 0x2A96336C, 0x9954385E, 0xAAE226BA, 0x92382E60,
        0x91E957B0, 0x8E888CF9, 0x17837218, 0x1E853F12, 0x44D5BFC3, 0xFAA85961, 0xE35E78D5, 0xC92E3410,
        0x9A6A5DA2, 0xC88B4F86, 0x6EBDAD1A, 0x00054975, 0x94F0A5BC, 0x23DB6F07, 0x27498498, 0x7013A64C,
        0xED5FE3AE, 0x282CCC83, 0x77F47B88, 0xE6CF29DE, 0xDDE6D146, 0xC33EAA2C, 0xF0350DC7, 0xD6332AD2,
        0xE0532343, 0x64022BF3, 0x0327DB94, 0x636D05EC, 0x2D8461ED, 0x066EFEB5, 0x3F1760D1, 0xAEC7B501,
        0xF8591797, 0x3BA75E03, 0xC06B1D26, 0x659C425F, 0x38A9192B, 0x4BF7BB22, 0x882D6427, 0xF724D7BE,
        0xDC0B65AC, 0xA83790E2, 0xCF5C473A, 0xD9099117, 0x15D05AC8, 0xB365D5D6, 0xC201CEB7, 0x45C3DF58,
        0x95C48BE1, 0x2C862D0B, 0xA256559D, 0x964AD376, 0x9D9DE689, 0x498C32A8, 0xAB73B368, 0x02FEE0A5,
        0x7BC110E3, 0x4382A748, 0x590E4DAF, 0xA70A30EE, 0x47AE94C1, 0x33557D53, 0xFE1D35FA, 0x1F9A50BF,
        0x7DF8E128, 0x6B30CB5A, 0x9B0318CB, 0xF3A26D81, 0x53217450, 0x073A9F19, 0x85604A38, 0xF1F67CA6,
        0x9F4EAE56, 0x7CEFEC79, 0x0115EE70, 0xFBCA25B9, 0xD732E225, 0x4D47C6CA, 0x0EE40747, 0x2E502FEA,
        0xB4777FF6, 0x0AFBD064, 0x5E973E1C, 0x04717E15, 0xCDDAD8A7, 0xA4DD5469, 0xDF61C314, 0x84C5C766,
        0x22AC683D, 0x80239A6B, 0x71D102F8, 0xDA7E9587, 0x4C89C9DF, 0xB70C0085, 0xCAB3D411, 0x19A63D57,
        0x9CEC807B, 0x3CDCDADD, 0x8CE08A35, 0xD093A98B, 0x5A784E45, 0xE13F87B8, 0xC548F829, 0x817DBD6F,
        0xBCBF707F, 0x790479E4, 0x3A11B437, 0x89CE376D, 0xCC10894B, 0x21F5A365, 0xC192BC78, 0xA3A30C9B,
        0xB9C0B12D, 0xE92AF100, 0xA534581D, 0xA6F9FBCE, 0x8B41CA1B, 0x50D41BC2, 0xEFE38E5C, 0x29C25F0D,
        0xB864EFC6, 0x9063B77A, 0x6D4398B1, 0xEE91DE95, 0x1B46B0A4, 0xD3D2C52F, 0x26F2BEF0, 0xE28F8542,
    ],
]


# Odd -- we only use the first 2 of the above 8 boxes


# Pre-rotate (traditional, probably not super necessary)
SBOXES = [SBOXES]
for r in (8, 16, 24):
    l = 32 - r

    SBOXES.append([[((el << l) | (el >> r)) & 0xFFFFFFFF for el in box] for box in SBOXES[0]])


# Input is 16 elements of 32 bits each
def _Hash512(inlist, p0, p1, p2):
    editlist = list(inlist)

    editlist[0] ^= p0
    editlist[1] ^= p1
    editlist[2] ^= p2

    # print([hex(x) for x in editlist])

    boxnum = 0
    for boxrot, lookupshift in ((0, 0), (2, 16), (1, 24), (3, 8)):
        box0 = SBOXES[boxrot][boxnum]
        box1 = SBOXES[boxrot][boxnum + 1]

        for idx in range(16):
            lookup = (editlist[idx] >> lookupshift) & 0xFF
            if idx % 4 < 2:
                lookup = box0[lookup]
            else:
                lookup = box1[lookup]
            # print('lookup', hex(lookup))

            editlist[(idx + 1) % 16] ^= lookup
            editlist[(idx + 15) % 16] ^= lookup

        # print([hex(x) for x in editlist])

    editlist[14] ^= p0
    editlist[13] ^= p1
    editlist[12] ^= p2

    retval = [inlist[0] ^ editlist[15],
        inlist[1] ^ editlist[14],
        inlist[2] ^ editlist[13],
        inlist[3] ^ editlist[12]]

    # print('Iteration of _Hash512', ' '.join(hex(x) for x in retval))

    return retval


def snefru(inbytes):
    if len(inbytes) % 64:
        raise ValueError('Input length must be a multiple of 64 bytes (is %d)' % len(inbytes))

    p0 = 0
    p1 = 0
    p2 = len(inbytes) * 8

    temp_output = [0] * 16
    output_loc = 0
    for offset in range(0, len(inbytes), 64):
        grist = struct.unpack_from('>16L', inbytes, offset)
        temp_output[output_loc:output_loc+4] = _Hash512(grist, p0, p1, p2)
        p2 += 1
        output_loc += 4

        if output_loc >= 16:
            temp_output[0:4] = _Hash512(temp_output, p0, p1, p2)
            output_loc = 4
            p2 += 1

    return struct.pack('>4L', *_Hash512(temp_output, p0, p1, p2))


def append_snefru(x):
    while len(x) % 64: x += b'\0' # this is a requirement of the hash
    return x + bytes(48) + snefru(x)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Append snefru hash to file')
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--align', type=int, default=64, action='store', help='align the final product to a multiple of this (must be multiple of 64)')

    args = parser.parse_args()
    x = open(args.input, 'rb').read()
    while len(x) % args.align != args.align - 64: x += b'\0'
    x = append_snefru(x)
    open(args.output, 'wb').write(x)
