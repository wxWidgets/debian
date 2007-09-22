/////////////////////////////////////////////////////////////////////////////
// Purpose:     XML resources editor
// Author:      Vaclav Slavik
// Created:     2000/05/05
// RCS-ID:      $Id: treedt.h,v 1.3.2.1 2005/06/20 17:35:35 MR Exp $
// Copyright:   (c) 2000 Vaclav Slavik
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _TREEDT_H_
#define _TREEDT_H_


#include "wx/treectrl.h"

class WXDLLEXPORT wxXmlNode;

class XmlTreeData : public wxTreeItemData
{
    public:
        XmlTreeData(wxXmlNode *n) : Node(n) {}        
        wxXmlNode *Node;
};


#endif
