import utilities as u

print(
  ('Elite Decryptor:')+
  ('\n--------------------------')+
  ('\n(type \'--exit\' to quit)\n')
)

while True:
  message = input('(encrypted message)> ')
  if message == '--exit':
    break
  num = int(input('(2nd number in captured packet)> '))
  print(f"\n(decrypted message)> {u.decrypt(message, num)}\n")
