def fractional_browning_motion(octaves, noise, persistence, x, y):
    output = 0.0

    for octave in range(octaves):
        frequency = 2**octave
        amplitude = persistence**octave

        output = output + noise.apply(x * frequency, y * frequency) * amplitude

    return output
