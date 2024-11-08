"""
Addressable Paragraphs
------------------------
In converting from MD to html images are wrapped in <p> objects.
This plugin gives those paragraphs the 'img' class for styling enhancements.
"""

from __future__ import unicode_literals
from pelican import signals
from bs4 import BeautifulSoup

def content_object_init(instance):

    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content, 'html.parser')

        for p in soup(['p', 'object']):
                if p.findChild('img'):
                    # Grab image source and check if it's scalable
                    img_src = p.img['src']
                    if 'scalable' in img_src:
                        p.attrs['class'] = 'scalable-img'
                    else:
                        # Otherwise, add vanilla 'img' class to the p tag
                        p.attrs['class'] = 'img'

                    # Add caption
                    caption = soup.new_tag('span',**{'class':'caption'})
                    for i in reversed(p.contents):
                        if i.name != 'img': #if it is not an <img> tag
                            caption.insert(0,i.extract())
                    p.append(caption)

        instance._content = soup.decode()


def register():
    signals.content_object_init.connect(content_object_init)
