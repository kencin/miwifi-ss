#!/usr/bin/python
# -*- coding: UTF-8 -*-  
# deepLearning - dnsmasq.py
# 2019/3/17 21:43
# Author:Kencin <myzincx@gmail.com>
import re
import os
import datetime
import base64
import shutil
import urllib.request

mydnsip = '208.67.222.222'
mydnsport = '443'

# the url of gfwlist
baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
# match comments/title/whitelist/ip address
comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'
tmpfile = 'gfwlisttmp'
# do not write to router internal flash directly
rulesfile = 'gfwlist.conf'

with open(rulesfile, 'w', encoding="UTF-8") as f:
    f.write('# gfw list ipset rules for dnsmasq\n')
    f.write('# updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    f.write('#\n')


print('fetching list...')

content = urllib.request.urlopen(baseurl, timeout=3).read()
content = base64.b64decode(content)

# write the decoded content to file then read line by line
# tfs = open(tmpfile, 'w')
# tfs.write(content)
# tfs.close()
with open(tmpfile, 'w', encoding="UTF-8") as f:
    f.write(content.decode("utf-8"))

file = open(tmpfile, 'r')

print('page content fetched, analysis...')


# remember all blocked domains, in case of duplicate records
domainlist = []

for line in file.readlines():
    if re.findall(comment_pattern, line):
        pass
    # fs.write('#' + line)
    else:
        domain = re.findall(domain_pattern, line)
        if domain:
            try:
                found = domainlist.index(domain[0])
                print(domain[0] + ' exists.')

            except ValueError:
                print('saving ' + domain[0])
                domainlist.append(domain[0])
                with open(rulesfile, 'a', encoding="UTF-8") as f:
                    f.write('server=/.%s/%s#%s\n' % (domain[0], mydnsip, mydnsport))
                    f.write('ipset=/.%s/gfwlist\n' % domain[0])
        else:
            print('no valid domain in this line: ' + line)

file.close()
print('Done! Please restart dnsmasq')
print('exec /etc/init.d/dnsmasq restart')


# print('restart dnsmasq...')
#
# print(os.popen('/etc/init.d/dnsmasq restart').read())
