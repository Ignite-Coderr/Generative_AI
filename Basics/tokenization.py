import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o')

print("Vocab Size:", encoder.n_vocab)   #Vocab Size: 200019

text = "The cat sat on the mat"

# Tokenize the text
tokens = encoder.encode(text)

print("Tokens:", tokens)  # Tokens: [976, 9059, 10139, 402, 290, 2450]

decoded = encoder.decode([976, 9059, 10139, 402, 290, 2450])
print("Decoded Text:", decoded)  # Decoded Text: The cat sat on the mat

e
# TODO: Generating Vector embedding for the text so to have the semnatic understanding of the 
# text and to perform the similarity search based on the vector embedding.
