import struct


def readTCK(filepath, verbose=False):
    with open(filepath, 'rb') as f:
        data = f.read()
    header_end = 0
    while data[header_end:header_end+3].decode("utf-8") != 'END':
        header_end += 1
    header_raw = data[:header_end+3].decode("utf-8").split('\n')
    header = dict()
    command_history = list()
    for item in header_raw:
        if item == 'END':
            break
        elif len(item) > 12 and item[:13] == 'mrtrix tracks':
            header['first_line'] = 'mrtrix tracks'
        elif item.split(':')[0] == 'command_history':
            command_history.append(item.split(':')[1][1:])
        else:
            header[item.split(':')[0]] = item.split(':')[1][1:]
    header['command_history'] = command_history

    if verbose:
        file_count = str()
        for char in header['count']:
            if char.isdigit():
                file_count += char
        file_count = int(file_count)
        print('Header reading complete and file data open...')

    file_offset = str()
    for char in header['file']:
        if char.isdigit():
            file_offset += char

    if 'LE' in header['datatype']:
        endian = 'LE'
    else:
        endian = 'BE'

    if '32' in header['datatype']:
        bytesize = 4
    else:
        bytesize = 8

    file_offset = int(file_offset)
    rawtracts = list()
    i = -1
    infinities = 0
    nans = 0
    done = False
    rawtract = list()

    if verbose:
        print('Starting tract extraction...')

    while not done:
        i += 1
        offset = i*bytesize
        eightbytes = bytearray(data[file_offset+offset:file_offset+bytesize+offset])

        if endian == 'LE':
            eightbytes.reverse()

        val = struct.unpack('!f', bytes.fromhex(eightbytes.hex()))[0]

        if eightbytes.hex() == '7f800000':
            infinities += 1

        if val != val:
            nans += 1
        else:
            rawtract.append(val)

        if nans == 3:
            nans = 0
            rawtracts.append(rawtract)
            rawtract = list()

        if infinities == 3:
            done = True
        
        if verbose and i % 10000 == 1:
            print(str((len(rawtracts)/file_count)*100)+'%', 'of tracts extracted...')

    if verbose:
        print('Raw tracts extracted, counted', str(len(rawtracts)), 'tracts...')
        print('Converting to correct format...')

    tracts = list()
    for tract in rawtracts:
        finaltract = list()
        vertices = int(len(tract)/3)
        for j in range(vertices):
            x = tract[0+(j*3)]
            y = tract[1+(j*3)]
            z = tract[2+(j*3)]
            finaltract.append((x, y, z))
        tracts.append(finaltract)
    
    if verbose:
        print('File read completed!')

    return header, tracts
