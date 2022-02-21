import struct # For working with byte to float coversions


def readTCK(filepath, verbose=False):
    # Takes in a filepath to a .tck file and extracts the file data.
    # Setting the function as verbose prints progress data!

    # Open the file
    with open(filepath, 'rb') as f:
        data = f.read()

    # Extracting raw file header
    header_end = 0
    while data[header_end:header_end+3].decode("utf-8") != 'END':
        header_end += 1
    header_raw = data[:header_end+3].decode("utf-8").split('\n')

    # Extracting command history and creating header
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

    # Generating some values for calculating progress in talkative code...
    if verbose:
        file_count = str()
        for char in header['count']:
            if char.isdigit():
                file_count += char
        file_count = int(file_count)
        print('Header reading complete and file data open...')

    # Extracting data byte offset
    file_offset = str()
    for char in header['file']:
        if char.isdigit():
            file_offset += char
    
    # Determining if data is stored in big endian or little endian
    if 'LE' in header['datatype']:
        endian = 'LE'
    else:
        endian = 'BE'

    # Determining if data is stored in 32 or 64 bit floats
    if '32' in header['datatype']:
        bytesize = 4
    else:
        bytesize = 8

    # Defining and converting some important variables:
    file_offset = int(file_offset)
    rawtracts = list()
    i = -1
    infinities = 0
    nans = 0
    done = False
    rawtract = list()

    # Some more talkative code...
    if verbose:
        print('Starting tract extraction...')

    # Extracting tracts
    while not done:

        # Iterate byte position and get next 8 bytes
        i += 1
        offset = i*bytesize
        eightbytes = bytearray(data[file_offset+offset:file_offset+bytesize+offset])

        # Reverse byte order if little endian
        if endian == 'LE':
            eightbytes.reverse()

        # Convert to floating point value
        val = struct.unpack('!f', bytes.fromhex(eightbytes.hex()))[0]

        # If byte is Inf, add one to Inf count (three Inf bytes means end of file!)
        if eightbytes.hex() == '7f800000':
            infinities += 1

        # See if byte is NaN in a clever way!
        if val != val:
            nans += 1
        else:
            rawtract.append(val)

        # If byte is NaN, add one to NaN count (three Nan bytes means end of tract!)
        if nans == 3:
            nans = 0
            rawtracts.append(rawtract)
            rawtract = list()

        # If there have been three Inf bytes then end of file is reached!
        if infinities == 3:
            done = True
        
        # Some more talkative code with progress included...
        if verbose and i % 10000 == 1:
            print(str((len(rawtracts)/file_count)*100)+'%', 'of tracts extracted...')

    # Some more talkative code...
    if verbose:
        print('Raw tracts extracted, counted', str(len(rawtracts)), 'tracts...')
        print('Converting to correct format...')

    # Create a list of tracts and populate it with coordinates of vertices in format [(X1, Y1, Z1), (X2, Y2, Z2), ...]
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
    
    # Some more talkative code...
    if verbose:
        print('File read completed!')

    # Return both the header dictionary and the tract data
    return header, tracts
