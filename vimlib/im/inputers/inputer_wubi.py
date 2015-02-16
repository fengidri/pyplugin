# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 14:49:41
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import urllib2
import json

import pyvim
import im.imrc as imrc

from inputer_base import IM_Base 
import logging
class _wubi_seach( object ):
    def __init__(self):
        self.cache={  }


    def search_from_db(self, patten):
        try:
            r = urllib2.urlopen("http://localhost/wubi/search?patten=%s" %
                patten)
            return json.loads(r.read())
        except Exception, e:
            pyvim.echoline(str(e))
            return ([], [])


    def search( self , patten):
        '得到备选的字词'
        words= self.cache.get( patten )
    
        if  words:
            return words

        w = self.search_from_db(patten)
        self.cache[ patten ] = w

        return w
    def setcount(self, patten, num):
        w, ass = self.cache.pop(patten)
        if len(w) -1 < num:
            return
        ww = w[num]
        url = "http://localhost/wubi/setcount?patten=%s&word=%s" % (patten,
                ww.encode('utf8'))
        try:
            urllib2.urlopen(url)
        except Exception, e:
            pyvim.echoline(str(e))

    def wubi(self, patten):
        return self.result(patten, *self.search(patten)) 

    def result(self, patten, words, associate):
        '组成vim 智能补全要求的形式，这一步只是py形式的数据，vim要求是vim的形式'

        items=[{"word": " " ,"abbr":"%s                  " %  patten }]

        if len( patten ) > 4:
            return items

        i = 0
        for w in words:
            i += 1
            items.append({"word":w, "abbr":"%s.%s"%(i, w)})

        for w, k, c  in associate:
            i += 1
            items.append(
                    {"word":w, 
                        "abbr":"%s.%s %s"%(i, w, k)}
                    )

        return items

class IM_Wubi( IM_Base, _wubi_seach):
    def __init__(self, areas = ['String', 'Comment']):
        IM_Base.__init__(self)
        _wubi_seach.__init__(self)
        self.index = 0
        self.buffer=[]
        self.pmenu = pyvim.SelMenu()
        self.AREAS = areas

    def cb_backspace(self):
        if not pyvim.pumvisible():
            pyvim.feedkeys('\<bs>', 'n')
            return 0

        if len( self.buffer ) > 1:
            self.buffer.pop()
            self.patten = ''.join(self.buffer)
            self.pmenu.show(self.wubi(self.patten), 0)
        else:
            del self.buffer[:]
            self.pmenu.cencel( )

   
    def cb_enter(self):
        if pyvim.pumvisible():
            pyvim.feedkeys(r'%s\<C-e>' % self.patten,'n')
            del self.buffer[ : ]
            return 0
        pyvim.feedkeys(r'\<cr>' ,'n')

    def cb_space(self): 
        del self.buffer[:]
        if pyvim.pumvisible():
            self.pmenu.select( 1 )
            return 0
        pyvim.feedkeys('\<space>', 'n')

    def cb_esc( self ):
        del self.buffer[:]
        pyvim.feedkeys( '\<esc>','n')

    def im(self, key):
        area = pyvim.syntax_area()

        if not (area in self.AREAS or '*' in self.AREAS):
            return
        logging.error("wubi:area: %s, %s", area, self.AREAS)
        


        self.key = key
        if imrc.count - self.index!= 1:  # 保证连续输入
            del self.buffer[:]
        self.index = imrc.count

        if key in self.cbs: #如果有对应的重载方法
            self.cbs.get(key)()

        elif key in imrc.digits:
            self.digit()

        elif key in imrc.lowerletter:
            self.lower_letter()

        elif key in imrc.upperletter:
            self.upper_letter()

        elif key in imrc.puncs: # 符号key
            self.output(imrc.puncs[key][0])
        return True

    def digit( self ):
        if pyvim.pumvisible():

            self.setcount(self.patten, int(self.key) -1)
            self.pmenu.select( int(self.key) )
            del self.buffer[:]
            return 0
        pyvim.feedkeys( self.key ,'n')

    def upper_letter( self ):
        del self.buffer[:]
        pyvim.feedkeys( self.key  ,'n' )

    def lower_letter( self ):
        self.buffer.append( self.key )
        self.patten = ''.join(self.buffer)
        self.pmenu.show(self.wubi(self.patten), 0)


if __name__ == "__main__":
    pass

