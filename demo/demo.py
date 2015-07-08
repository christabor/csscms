from csscms import InputBuilder

try:
    print('[DEBUG] Running demo')
    InputBuilder('test-inputs.css').generate().save('inputs.html')
except IOError:
    print('[ERROR] Could not load file or generate inputs')
