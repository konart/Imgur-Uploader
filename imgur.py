#!/usr/bin/python
 
from sys import argv
from StringIO import StringIO
from xml.dom import minidom
import pycurl, os, gtk, webbrowser
 
class SendToImgur():
 
    def parseXML(self, xml):
        xmldoc = minidom.parse(StringIO(xml))
        return xmldoc.getElementsByTagName("imgur_page")[0].firstChild.data
 
    def upload(self, file):
        c = pycurl.Curl()
        values = [("key", "YOUR_API_KEY"), ("image", (c.FORM_FILE, file))]
        c.setopt(c.URL, "http://imgur.com/api/upload.xml")
        c.setopt(c.HTTPPOST, values)
        buf = StringIO()
        c.setopt(pycurl.WRITEFUNCTION, buf.write)
        try:
            c.perform()
        except pycurl.error:
            return False
        return self.parseXML(buf.getvalue().strip())
 
sti = SendToImgur()
output = sti.upload(argv[1])
if output:
    webbrowser.open_new_tab(output)
    os.system('notify-send -i /usr/share/icons/imgur.png "Imgur" "Image has been uploaded"')
else:    
    os.system('notify-send -i /usr/share/icons/imgur.png "Imgur" "Error: cannot upload the image"')
