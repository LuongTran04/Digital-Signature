

import hashlib
import random
import math
import sys
from sympy import mod_inverse, nextprime
sys.set_int_max_str_digits(50000)

first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
					31, 37, 41, 43, 47, 53, 59, 61, 67,
					71, 73, 79, 83, 89, 97, 101, 103,
					107, 109, 113, 127, 131, 137, 139,
					149, 151, 157, 163, 167, 173, 179,
					181, 191, 193, 197, 199, 211, 223,
					227, 229, 233, 239, 241, 251, 257,
					263, 269, 271, 277, 281, 283, 293,
					307, 311, 313, 317, 331, 337, 347, 349]

def nBitRandom(n):
	return random.randrange(2**(n-1)+1, 2**n - 1)

def getLowLevelPrime(n):
	while True:
		pc = nBitRandom(n)
		for divisor in first_primes_list:
			if pc % divisor == 0 and divisor**2 <= pc:
				break
		else:
			return pc

def isMillerRabinPassed(mrc):
	maxDivisionsByTwo = 0
	ec = mrc - 1
	while ec % 2 == 0:
		ec >>= 1
		maxDivisionsByTwo += 1
	assert(2**maxDivisionsByTwo * ec == mrc - 1)

	def trialComposite(round_tester):
		if pow(round_tester, ec, mrc) == 1:
			return False
		for i in range(maxDivisionsByTwo):
			if pow(round_tester, 2**i * ec, mrc) == mrc - 1:
				return False
		return True

	numberOfRabinTrials = 20
	for _ in range(numberOfRabinTrials):
		round_tester = random.randrange(2, mrc)
		if trialComposite(round_tester):
			return False
	return True

def generate_large_prime(n):
	while True:
		prime_candidate = getLowLevelPrime(n)
		if isMillerRabinPassed(prime_candidate):
			return prime_candidate

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def generate_key_pair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def encrypt(pk, plaintext):
    key, n = pk
    return [pow(ord(char), key, n) for char in plaintext]

def decrypt(pk, ciphertext):
    key, n = pk
    return ''.join([chr(pow(char, key, n)) for char in ciphertext])

def message_to_number(message):
    """Convert a string message to a large integer."""
    return int.from_bytes(message.encode(), byteorder='big')

def sign(private_key, message):
    """Sign a message with the private key."""
    key, n = private_key
    message_hash = message_to_number(message)
    signature = pow(message_hash, key, n)
    return signature

def verify(public_key, message, signature):
    """Verify a message signature with the public key."""
    key, n = public_key
    message_hash = message_to_number(message) % n
    hash_from_signature = pow(signature, key, n)
    return message_hash == hash_from_signature

if __name__ == '__main__':
    print("Generating two large 512-bit prime numbers (this may take a while)...")
    # p = generate_large_prime(8192)
    # q = generate_large_prime(8192)
    p = 919951799372345419663571127018174985220094872998973360108303633009137739498549459420039305251792145092341609744473177679068257841659546463626310715618295950921278548451841790718828155043422792046553806193333979168561724176585654691017002220479973876719962898784514701949131301366585278018569418166994937570176032936321542229237823995968035401925459199522114379976054921161603858593295059302412235440418540766473046921677328497369750361706919417579922231559062852388367507192746693949584673069158550890325709296176813487641947593899318138267509472537673697754059303964583731187212564623888560280754462606436702474936940551315775907199539765487444160020053886738691098496880847590005241072228253205026629181635982041138173521425936335001320293355619289826759421549281621831956610669587466433131817612044976813267809830324658585231018640787935135865417643952461074691655959501127910881827762674128465304876669439626511676075728956747979028425657604794288705106614841786529585429401823701023389979780359811025915147168500076034454379064976256181227974765582117863565550247659479778983613573581078051347081681321427116470630032973488655018357079225451242442433884090435837260543649690654048149712517626829539695440476001840308696675949733706405722355020093173735098941786181137785588522725290076643136116445704577821409686542302803222086220914720991144254619010849964148026761260833102644365106290538704496139191458399818936802092199084805228487187397437711891384522748752578471072685642175565827586346446372535980560827366913486652062868000839424057447643260271317294174118474463372841573845780251786896996286009102567332977464943213417869834630728423165618939227944138926774304162021114197254718596292439452523166721972946859327668350743153076922996980350115585319819588117939187187888571850585650281806900581944135262493894411051204600811309742732680278505137239198150769901262867574837616067801543064517554492888906536338715153221205652410901780670171655008203063684818595371596742070429489012227142203725063434275923104144173298458760327573572612828979707438042854954546122531314197208957740410148272141997072543606316231956384026844959837169578988710135867035842186007173606275153223591520992002311818556546532089449428224551069523913555927847860068685470921717345913414889144445689363218244925806402402846974887168471572926195141655630849556729155613691583598303897354875930323911976945993891490362405914586547735359064101959123128536936160241950104987361238822859
    q = 847045645857194970117227853283316656225265651225920018761746349255864212794502245482692791851759016711359781578281496134217330503092842056922767162059828139199008677677588197140880474706550192271095211092991039440092467980929206646573031652959681911647722233556749295982467871201706374895680916470661166607400915664112777103133100195373262634006527224665072658040219208559806339581482037519592974984610215994216185312526983946192402175130680880788247063094926037285152300767240179235327875893971405607117029606694247284713360780881116904495377511636472032423418564381832978818825157589489395120091655985674325791412117752357851145512098987761384251871360677958957173098151232787474558534073614137612919888580755320527906998457119639899734465386934757683425813294020224718537875211083424687114497925249764648399658524169742883656611926499823133219012047319056415685511656807167478064486190491377144122195740794613641551671530418927926620454974169355570283254004108044057960315701670856334290623235861487544478789964746941261299107876136443386514357405288187945344477581310359508760746748693632957986820254864757979987765449969954919488315046126337978466675135550020667100137159004765083751905771945556118932967021719268802487870080046785459539816456796472997439061848026731606679697765084735515486235337515277974405358911286411346343075781677326005368541592642296100741055675847698299449141423995999898292961245546028928000763819678392306788881294864052081188612825631495873844908749202613940894540790333068135211976569477328643195465397654510681570912660619194396611099864419581578369200242179972518123394313653209204498483836785894163845541401323011026964670238948683704598612760936614413047024682738016139440490108715178640232655343439601672320840473504444444805731153061075548119745031005329709557429987955371176493164351211335295476531355253913784983251287787004399230424239555718989360424716715990619496375888273491774534877342182221833208936034128900181789838682121379030355826217319656548582448645940384437184049702559223169772472227238462420563895339343896343389976708163488871148390897910185388376160039816347413319228508014187151269846319964893400390571556055668032772495165314454494984828717604410032075978598920663690164044065868071632756763960180269617821498094424030586627066665390926004513962233607928411530535135215305784042499661605076623394653880525299975466620670212365907216307529955820493022302703799089011801612290113730741770406850186810886481
   
    print(f"p = {p}")
    print(f"q = {q}")
    print("Generating public/private key pairs...")
    public, private = generate_key_pair(p, q)

    print("Your public key is ", public)
    print("Your private key is ", private)

    message = input("Enter a message to encrypt with your public key: ")
    encrypted_msg = encrypt(public, message)

    print("Your encrypted message is: ", ''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with private key ", private)
    print("Your message is: ", decrypt(private, encrypted_msg))
    number = message_to_number(message)
    signature = sign(private, message)
    print(f"signature: {signature}")
    print(f"verify: {verify(public, message, signature)}")
    
