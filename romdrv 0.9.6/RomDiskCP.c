#include <A4Stuff.h>#include <Devices.h>#define kOnButton 2#define kOffButton 3#define kRAMButton 6#define kROMButton 7#pragma parameter __D0 ReadXPRam(__D0, __D1, __A0)short ReadXPRam(short size, short offset, char *where) = {0x4840, 0x3001, _ReadXPRam};#pragma parameter __D0 WriteXPRam(__D0, __D1, __A0)short WriteXPRam(short size, short offset, char *where) = {0x4840, 0x3001, _WriteXPRam};void updateDisplay(DialogPtr d, short numItems, char startup, char ram, char grayed);void updateDisplay(DialogPtr d, short numItems, char startup, char ram, char grayed) {	GrafPtr savePort;	Handle h;	Rect r;	short type;		GetPort(&savePort);	SetPort(d);	GetDItem(d, kOnButton+numItems, &type, &h, &r);	SetCtlValue((ControlHandle)h, startup);	GetDItem(d, kOffButton+numItems, &type, &h, &r);	SetCtlValue((ControlHandle)h, !startup);	GetDItem(d, kRAMButton+numItems, &type, &h, &r);	SetCtlValue((ControlHandle)h, ram);	GetDItem(d, kROMButton+numItems, &type, &h, &r);	SetCtlValue((ControlHandle)h, !ram);	SetPort(savePort);	return;}pascal long main(short message,short item,short numItems,short /*privateValue*/,			     EventRecord *e, void *cdev, DialogPtr d){	EnterCodeResource();	long result;	Handle h;	Rect r;	short type;	GrafPtr savePort;	unsigned char **via1ptr = (unsigned char**)0x01D4;	unsigned char data, dir;	char startup = 0;	char ram = 0;	result = (long)cdev;		switch (message) {	case initDev:		cdev = (Handle)cdevUnset;		ReadXPRam(1, 4, &startup);		ReadXPRam(1, 5, &ram);		result = (long)cdev;		break;	case closeDev:		cdev = (Handle)cdevUnset;		result = cdevUnset;		break;	case macDev:		result = 1L;		break;	case updateDev:	case activDev:		ReadXPRam(1, 4, &startup);		ReadXPRam(1, 5, &ram);		updateDisplay(d, numItems, startup, ram, 0);		break;	case deactivDev:		ReadXPRam(1, 4, &startup);		ReadXPRam(1, 5, &ram);		updateDisplay(d, numItems, startup, ram, 1);		break;	case hitDev:		ReadXPRam(1, 4, &startup);		ReadXPRam(1, 5, &ram);		switch(item-numItems) {		case kOnButton: startup = 1; break;		case kOffButton: startup = 0; break;		case kRAMButton: ram = 1; break;		case kROMButton: ram = 0; break;		default: break;		};		updateDisplay(d, numItems, startup, ram, 0);		WriteXPRam(1, 4, &startup);		WriteXPRam(1, 5, &ram);		break;	default:		break;	};			ExitCodeResource();		return result;}