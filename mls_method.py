def lfsr(seed, taps):
    sr, xor = seed, 0
    seqn = []
    while 1:
        for t in taps:
            xor += int(sr[t-1])
        if xor%2 == 0.0:
            xor = 0
        else:
            xor = 1
        # Transform Seq from "0 to 1" to "-1 to 1"
        if xor == 1:
            seqn.append(-1)
        else:
            seqn.append(1)
            
        sr, xor = str(xor) + sr[:-1], 0
        # print sr
        if sr == seed:
            return seqn
            break

def mls_gen(rt60, fs):
    import math

    seed=0
    
    # rt60 in msec, fs in hz

    t_len = rt60/500.0 # time length, twice as long as rt60 in sec

    s_len = t_len*fs # sample length, time length * sampling frequency

    n_taps =int(round(math.log(s_len,2)+0.5)) # length of shift register rounded up
    print n_taps
    i=0

    while i<n_taps : # Creating and filling the seed 
        seed=seed+pow(10,i)
        # debug print seed
        i=i+1

    # taps_list taken from "Messung von Impulseantworten mit Pseudo-Noise Sequenzen"
    # Diplomarbeit by Udo Barth University Bremen 1998
    taps_list = [[0,0],[0,0],[2,1],[3,1],[4,1],
                 [5,2],[6,1],[7,1],[8,6,5,1],
                 [9,4],[10,3],[11,2],[12,7,4,3],
                 [13,4,3,1],[14,12,11,1],[15,11],
                 [16,5,3,2],[17,14,13,9],[18,7],
                 [19,6,5,1],[20,3],[21,2],[22,1],
                 [23,5],[24,4,3,1],[25,3],[26,8,7,1],
                 [27,8,7,1],[28,3],[29,2],[30,16,15,1],
                 [31,3],[32,28,27,1],[33,13],[34,15,14,1],
                 [35,2],[36,11],[37,12,10,2],[38,6,5,1],
                 [39,4],[40,21,19,2]]
    
    mls=lfsr(str(seed),taps_list[n_taps])

    return mls

    
