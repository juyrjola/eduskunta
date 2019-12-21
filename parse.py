import glob
import re
from lxml import objectify

NSMAP = {
    'ns11': 'http://www.eduskunta.fi/skeemat/siirto/2011/09/07',
    'sa': 'http://www.arkisto.fi/skeemat/sahke2/2011/01/31_vnk',
    'ns4': 'http://www.eduskunta.fi/skeemat/siirtoelementit/2011/05/17',
    'asi': 'http://www.vn.fi/skeemat/asiakirjakooste/2010/04/27',
    'asi1': 'http://www.vn.fi/skeemat/asiakirjaelementit/2010/04/27',
    'jme': 'http://www.eduskunta.fi/skeemat/julkaisusiirtokooste/2011/12/20',
    'met': 'http://www.vn.fi/skeemat/metatietokooste/2010/04/27',
    'met1': 'http://www.vn.fi/skeemat/metatietoelementit/2010/04/27',
    'org': 'http://www.vn.fi/skeemat/organisaatiokooste/2010/02/15',
    'org1': 'http://www.vn.fi/skeemat/organisaatioelementit/2010/02/15',
    'sii': 'http://www.eduskunta.fi/skeemat/siirtokooste/2011/05/17',
    'sii1': 'http://www.eduskunta.fi/skeemat/siirtoelementit/2011/05/17',
    'sis': 'http://www.vn.fi/skeemat/sisaltokooste/2010/04/27',
    'sis1': 'http://www.vn.fi/skeemat/sisaltoelementit/2010/04/27',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'he': 'http://www.vn.fi/skeemat/he/2010/04/27',
    'mix': 'http://www.loc.gov/mix/v20',
    'narc': 'http://www.narc.fi/sahke2/2010-09_vnk',
    'saa': 'http://www.vn.fi/skeemat/saadoskooste/2010/04/27',
    'saa1': 'http://www.vn.fi/skeemat/saadoselementit/2010/04/27',
    'tau': 'http://www.vn.fi/skeemat/taulukkokooste/2010/04/27',
    'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
    'fra': 'http://www.eduskunta.fi/skeemat/fraasikooste/2011/01/04',
    'fra1': 'http://www.eduskunta.fi/skeemat/fraasielementit/2011/01/04',
    'vsk1': 'http://www.eduskunta.fi/skeemat/vaskielementit/2011/01/04',
    'evek': 'http://www.eduskunta.fi/skeemat/vastaus/2011/01/04',
    'vsk': 'http://www.eduskunta.fi/skeemat/vaskikooste/2011/01/04',
    'eka': 'http://www.eduskunta.fi/skeemat/eduskuntaaloite/2012/08/10',
    'kys': 'http://www.eduskunta.fi/skeemat/kysymys/2012/08/10',
    'elu': 'http://www.eduskunta.fi/skeemat/ehdotusluettelo/2014/07/28',
    'ptk': 'http://www.eduskunta.fi/skeemat/poytakirja/2011/01/28',
    'vml': 'http://www.eduskunta.fi/skeemat/mietinto/2011/01/04',
    'vas': 'http://www.eduskunta.fi/skeemat/vastalause/2011/01/04',
    'kks': 'http://www.eduskunta.fi/skeemat/kokoussuunnitelma/2011/01/28',
    'til': 'http://www.eduskunta.fi/skeemat/tilasto/2013/04/24',
    'kir': 'http://www.vn.fi/skeemat/kirjelma/2010/04/27',
    'vpa': 'http://www.eduskunta.fi/skeemat/kasittelytiedotvaltiopaivaasia/2011/03/25',
    'buk': 'http://www.vn.fi/skeemat/talousarviokooste/2011/06/14',
    'buk1': 'http://www.vn.fi/skeemat/talousarvioelementit/2011/06/14',
    'tam': 'http://www.eduskunta.fi/skeemat/talousarviokirjelma/2011/06/14',
    'lka': 'http://www.eduskunta.fi/skeemat/kasittelytiedotlausumaasia/2013/11/15',
}


def find_missing_namespaces():
    all_uris = set(NSMAP.values())
    for xml_file in glob.glob('xml/*/*/*.xml'):
        f = open(xml_file, 'r')
        out = objectify.parse(f)
        for ch in out.iter():
            ns = set(ch.nsmap.values())
            new_uris = ns - all_uris
            for uri in new_uris:
                for key, val in ch.nsmap.items():
                    if val == uri:
                        print("    '%s': '%s'" % (key, val))
                        break
                else:
                    assert False
            all_uris |= new_uris


def replace_ns(s):
    def replace(ns):
        ns = ns.groups()[0].strip('{}')
        for key, val in NSMAP.items():
            if val == ns:
                return '%s:' % key
        return ns.groups()[0]
    return re.sub(r'^(\{.*\})', replace, s)


def fix_attrib(elem):
    ret = {replace_ns(key): val for key, val in elem.attrib.items()}
    elem.attr = ret
    return elem


def xpath(elem, path: str):
    return [fix_attrib(x) for x in elem.xpath(path, namespaces=NSMAP)]


def find(elem, path: str):
    ret = elem.find(path, namespaces=NSMAP)
    if ret is not None:
        return fix_attrib(ret)


def findall(elem, path: str):
    return [fix_attrib(x) for x in elem.findall(path, namespaces=NSMAP)]


s = open('xml/GovernmentProposal_fi/2018/2018-11-16T10:21:27.749000+02:00.xml', 'r').read()
doc = objectify.fromstring(s)
obj = xpath(doc, '//jme:JulkaisuMetatieto')[0]
print(obj.attr)
