from csscms.parser import InputBuilder
import os

# try:
print('[DEBUG] Running demo')
name = raw_input('Which one (choose a number)?'
                 '\n1. Bootstrap3 \n2. Font-awesome \n3. Test\n=> ')


output = {
    '1': 'bootstrap3',
    '2': 'fa',
    '3': 'test-inputs',
    '4': 'simple'
}
InputBuilder('{}/{}.css'.format(
    os.getcwd(), output[name])).generate().save(
        '{}-output.html'.format(output[name]))
# except IOError:
#     print('[ERROR] Could not load file or generate inputs')
