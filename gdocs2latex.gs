// Based on http://github.com/mangini/gdocs2md

function ConvertToSimpleLatex() {
  var numChildren = DocumentApp.getActiveDocument().getActiveSection().getNumChildren();
  var text = '';
  var attachments = [];
  var inItemize = false;
  var inEnumerate = false;

  // Walk through all the child elements of the doc.
  for (var i = 0; i < numChildren; i++) {
    var child = DocumentApp.getActiveDocument().getActiveSection().getChild(i);
    var result = processParagraph(i, child);
    if (result !== null) {
      if (result && result.length > 0) {
        if (starts(result, '{itemize}') || starts(result, '{enumerate}')) {
          if (starts(result, '{itemize}')) {
            line = result.substring(9);
            if (!inItemize) {
              text += '\\begin{itemize}\n'
              inItemize = true;
            }
            text += '\\item ' + line
          } else {  // enumerate
            line = result.substring(11);
            if (!inEnumerate) {
              text += '\\begin{enumerate}\n'
              inEnumerate = true;
            }
            text += '\\item ' + line
          }
        } else {
          if (inItemize) {
            text += '\\end{itemize}\n'
            inItemize = false;
          }
          if (inEnumerate) {
            text += '\\end{enumerate}\n'
            inEnumerate = false;
          }
          text += result
        }
        text += '\n';
      }
    }
  }

  attachments.push({'fileName': DocumentApp.getActiveDocument().getName() + '.txt', 'mimeType': 'text/plain', 'content': text});

  MailApp.sendEmail(Session.getActiveUser().getEmail(),
                    '[Automágica] ' + DocumentApp.getActiveDocument().getName(),
                    'Convertiste el adjunto a Latex simplificado para usar con Automágica (' + DocumentApp.getActiveDocument().getUrl() + ')' +
                    '\n\nMás información en http://www.juanjoconti.com/automagica/\n',
                    { 'attachments': attachments });
}

// Process each child element (not just paragraphs).
function processParagraph(index, element) {
  // First, check for things that require no processing.
  if (element.getNumChildren() == 0) {
    return null;
  }
  // TOC.
  if (element.getType() === DocumentApp.ElementType.TABLE_OF_CONTENTS) {
    return null;
  }

  // Set up for real results.
  var result = {};
  var pOut = '';
  var textElements = [];

  // Skip tables
  if (element.getType() === DocumentApp.ElementType.TABLE) {
    return null;
  }

  // Process various types (ElementType)
  for (var i = 0; i < element.getNumChildren(); i++) {
    var t = element.getChild(i).getType();

    if (t === DocumentApp.ElementType.TEXT) {
      var txt = element.getChild(i);
      pOut += txt.getText();
      textElements.push(txt);
    }
  }

  if (textElements.length == 0) {
    return result;
  }

  var prefix = findPrefix(element);
  var suffix = '';
  if (prefix.lastIndexOf('\\', 0) === 0) {
    suffix = '}'
  } else if (prefix == '\n\n') {
    suffix = '\n\n'
  }

  var pOut = '';
  for (var i = 0; i < textElements.length; i++) {
    pOut += processTextElement(textElements[i]);
  }

  return prefix + pOut + suffix;
}

// Add correct prefix to list items and headers.
function findPrefix(element) {
  var prefix='';
  if (element.getType() === DocumentApp.ElementType.PARAGRAPH) {
    var paragraphObj = element;
    switch (paragraphObj.getHeading()) {
      case DocumentApp.ParagraphHeading.HEADING4: prefix+='\\subsection*{'; break;
      case DocumentApp.ParagraphHeading.HEADING3: prefix+='\\section*{'; break;
      case DocumentApp.ParagraphHeading.HEADING2: prefix+='\n\n'; break;
      case DocumentApp.ParagraphHeading.HEADING1: prefix+='\\part*{'; break;
      default:
    }
  } else if (element.getType() === DocumentApp.ElementType.LIST_ITEM) {
      var listItem = element;
      var nesting = listItem.getNestingLevel();
      var gt = listItem.getGlyphType();
      // Bullet list (<ul>):
      if (gt == DocumentApp.GlyphType.BULLET
          || gt == DocumentApp.GlyphType.HOLLOW_BULLET
          || gt == DocumentApp.GlyphType.SQUARE_BULLET) {
        prefix = '{itemize}';
      } else {
        // Ordered list (<ol>):
        prefix = '{enumerate}';
      }
    }
  return prefix;
}

function processTextElement(txt) {
  if (typeof(txt) === 'string') {
    return txt;
  }

  var pOut = txt.getText();
  if (!txt.getTextAttributeIndices) {
    return pOut;
  }

  var attrs = txt.getTextAttributeIndices();
  var lastOff = pOut.length;

  for (var i = attrs.length - 1; i >= 0; i--) {
    var off = attrs[i];
    if (txt.isBold(off)) {
      var d1 = '\\textbf{'
      var d2 = '}';
      if (txt.isItalic(off)) {
        d1 = '\\textbf{\\textit{'; d2 = '}}';
      }
      pOut = pOut.substring(0, off) + d1 + pOut.substring(off, lastOff) + d2 + pOut.substring(lastOff);
    } else if (txt.isItalic(off)) {
      pOut = pOut.substring(0, off) + '\\textit{' + pOut.substring(off, lastOff) + '}' + pOut.substring(lastOff);
    }
    lastOff=off;
  }
  if (pOut == '*') {
    pOut = '\\begin{center} * \\end{center}';
  }
  return pOut;
}
