/////////////////////////////////////////////////////////////////////////////
// Name:        src/cocoa/ObjcRef.mm
// Purpose:     wxObjcAutoRefBase implementation
// Author:      David Elliott
// Modified by: 
// Created:     2004/03/28
// RCS-ID:      $Id: ObjcRef.mm 67254 2011-03-20 00:14:35Z DS $
// Copyright:   (c) 2004 David Elliott <dfe@cox.net>
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#include "wx/cocoa/ObjcRef.h"

#include <Foundation/NSObject.h>

/*static*/ struct objc_object* wxObjcAutoRefBase::ObjcRetain(struct objc_object* obj)
{
    return [obj retain];
}

/*static*/ void wxObjcAutoRefBase::ObjcRelease(struct objc_object* obj)
{
    [obj release];
}

