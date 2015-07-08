from csscms.parser import InputBuilder
import os

try:
    print('[DEBUG] Running demo')
    output = [
        'bootstrap3',
        'fa',
        'test-inputs',
        'simple'
    ]
    name = raw_input('Which one (choose a number)?\n{}\n=> '.format('\n'.join(
        ['{}: {} '.format(k + 1, v) for k, v in enumerate(output)])))

    filename = output[int(name) - 1]

    InputBuilder('{}/{}.css'.format(
        os.getcwd(), filename)).generate().save(
            '{}-output.html'.format(filename))

except IOError:
    print('[ERROR] Could not load file or generate inputs')
