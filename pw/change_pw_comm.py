"""
Let the user change the main PW password, that is used as key to encrypt
and decrypt other site password

This function must 
- change PW password, decode every site password and re encode with new 
  one
- change change of CHECK_PW file with a random string encoded with the 
  new PW password 
"""
# TODO 