import re, urllib, urllib2, urlparse
import csv

#**********************************************************************
# GoogleDriveDownloader
# Class that connects to Google Drive and downloads spreadsheets
#
# 2014, Miguel Carranza    miguel@miguelcarranza.es
# www.github.com/MiguelCarranza
#**********************************************************************
class GoogleDriveDownloader(object):

  def __init__(self, gmail_login, gmail_password):
    self.gmail_login = gmail_login
    self.gmail_password = gmail_password
    self.auth_token = self.__get_auth_token()



  #**********************************************************************
  # Private methods
  #**********************************************************************
  def __get_auth_token(self):
    url = 'https://www.google.com/accounts/ClientLogin'
    params = {
      "Email": self.gmail_login, 
      "Passwd": self.gmail_password,
      "service": 'wise',
      "accountType": "HOSTED_OR_GOOGLE",
      "source": 'ms-prometheus'
    }
    req = urllib2.Request(url, urllib.urlencode(params))
    return re.findall(r"Auth=(.*)", urllib2.urlopen(req).read())[0]


  def __get_headers(self):
    return {
              "Authorization": "GoogleLogin auth=" + self.auth_token,
              "GData-Version": "3.0"
           }


  def __get_key_and_gid(self, url):
    try:
      parsed_url = urlparse.urlparse(url)
      key = urlparse.parse_qs(parsed_url.query)['key'][0]
      gid = int(urlparse.parse_qs(parsed_url.fragment)['gid'][0])
    except:
      raise GoogleDriveDownloaderException('Wrong Google Drive URL.')

    return (key, gid)



  #**********************************************************************
  # Public methods
  #**********************************************************************
  def get_csv_file(self, url):
    key, gid = self.__get_key_and_gid(url)

    try:
      url_format = "https://docs.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=csv&gid=%i"
      headers = self.__get_headers()
      req = urllib2.Request(url_format % (key, gid), headers=headers)
      return urllib2.urlopen(req)
    except:
      raise GoogleDriveDownloaderException('Impossible to download %s.' % url)


  def get_csv_dict_reader(self, url):
    return csv.DictReader(self.get_csv_file(url))





#**********************************************************************
# GoogleDriveDownloaderException
#
# Exception. Used if something went wrong.
#**********************************************************************
class GoogleDriveDownloaderException(Exception):
  pass