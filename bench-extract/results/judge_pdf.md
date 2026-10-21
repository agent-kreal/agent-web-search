# scenario: pdf

## U1: https://arxiv.org/pdf/1706.03762
_(note: Attention is all you need)_

**[local-auto]** ERROR: unsupported/pdf

**[local-http]** ERROR: unsupported/pdf

**[local-curl]** ERROR: unsupported/pdf

**[local-browser]** ERROR: network/

**[firecrawl]** (1.51s, 32000 chars; wr=None, wo=None; hdr 3, code 0, links 8, lists 1)
```
# Attention Is All You Need

Ashish Vaswani∗

Google Brain
[avaswani@google.com](mailto:avaswani@google.com)

Noam Shazeer∗

Google Brain
[noam@google.com](mailto:noam@google.com)

Niki Parmar∗ Jakob Uszkoreit∗

Google Research Google Research
[nikip@google.com](mailto:nikip@google.com) [usz@google.com](mailto:usz@google.com)

Llion Jones∗

Google Research
[llion@google.com](mailto:llion@google.com)

**Aidan N. Gomez∗ †**
University of Toronto
[aidan@cs.toronto.edu](mailto:aidan@cs.toronto.edu)

Łukasz Kaiser∗

Google Brain
[lukaszkaiser@google.com](mailto:lukaszkaiser@google.com)

**Illia Polosukhin∗ ‡** [illia.polosukhin@gmail.com](mailto:illia.polosukhin@gmail.com)

## Abstract

The dominant sequence transduction models are based on complex recurrent or
convolutional neural networks that include an encoder and a decoder. The best
performing models also connect the encoder and decoder through an attention
mechanism. We propose a new simple network architecture, the Transformer,
based solely on attention mechanisms, dispensing with recurrence and convolutions
entirely. Experiments on two machine translation tasks show these models to
be superior in quality while being more parallelizable and requiring significantly
less time to train. Our model achieves 28.4 BLEU on the WMT 2014 Englishto-German translation task, improving over the existing best results, including
ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task,
our model establishes a new single-model state-of-the-art BLEU score of 41.8 after
training for 3.5 days on eight GPUs, a small fraction of the training costs of the
best models from the literature. We show that the Transformer generalizes well to
other tasks by applying it successfully to English constituency parsing both with
lar

[…середина…]

ed-forward network, which is applied to each position separately and identically. This
consists of two linear transformations with a ReLU activation in between.

$$
\\mathrm{FFN}(x)=\\max(0,xW\_{1}+b\_{1})W\_{2}+b\_{2}
$$

(2)

While the linear transformations are the same across different positions, they use different parameters
from layer to layer. Another way of describing this is as two convolutions with kernel size 1.
The dimensionality of input and output is _d_ model= 512, and the inner-layer has dimensionality
_d_ f f= 2048.

$$
d\_{model}=512
$$

$$
d\_{ff}=2048
$$

### 3.4 Embeddings and Softmax

Similarly to other sequence transduction models, we use learned embeddings to convert the input
tokens and output tokens to vectors of dimension _d_ model. We also use the usual learned linear transformation and softmax function to convert the decoder output to predicted next-token probabilities. In
our model, we share the same weight matrix between the two embedding layers and the pre-softmax
_√_
linear transformation, similar to \[30\]. In the embedding layers, we multiply those weights by _d_ model.

$$
d\_{model}
$$

$$
\\sqrt{d\_{model}}
$$

* * *

Table 1: Maximum path leng
```

**[tavily]** (1.32s, 32000 chars; wr=None, wo=None; hdr 4, code 0, links 0, lists 0)
```
## Provided proper attribution is provided, Google hereby grants permission to reproduce the tables and figures in this paper solely for use in journalistic or scholarly works. 

# Attention Is All You Need 

Ashish Vaswani ∗

Google Brain 

avaswani@google.com 

Noam Shazeer ∗

Google Brain 

noam@google.com 

Niki Parmar ∗

Google Research 

nikip@google.com 

Jakob Uszkoreit ∗

Google Research 

usz@google.com 

Llion Jones ∗

Google Research 

llion@google.com 

Aidan N. Gomez ∗ † 

University of Toronto 

aidan@cs.toronto.edu 

Łukasz Kaiser ∗

Google Brain 

lukaszkaiser@google.com 

Illia Polosukhin ∗ ‡ 

illia.polosukhin@gmail.com 

## Abstract 

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training dat

[…середина…]

ion dimension, k is the kernel size of convolutions and r the size of the neighborhood in restricted self-attention. Layer Type Complexity per Layer Sequential Maximum Path Length Operations Self-Attention O(n2 · d) O(1) O(1) 

Recurrent O(n · d2) O(n) O(n)

Convolutional O(k · n · d2) O(1) O(log k(n)) 

Self-Attention (restricted) O(r · n · d) O(1) O(n/r )

3.5 Positional Encoding 

Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence. To this end, we add "positional encodings" to the input embeddings at the bottoms of the encoder and decoder stacks. The positional encodings have the same dimension dmodel 

as the embeddings, so that the two can be summed. There are many choices of positional encodings, learned and fixed [9]. In this work, we use sine and cosine functions of different frequencies: 

P E (pos, 2i) = sin (pos/ 10000 2i/d model )

P E (pos, 2i+1) = cos (pos/ 10000 2i/d model )

where pos is the position and i is the dimension. That is, each dimension of the positional encoding corresponds to a sin
```

**[jina]** ERROR: {"error": "all fetch providers failed for https://arxiv.org/pdf/1706.03762: jina: jina network: [SSL: UNEXPECTED_EOF_WHI

**[parallel]** ERROR: {"error": "all fetch providers failed for https://arxiv.org/pdf/1706.03762: parallel: parallel fetch: network error: [SS

## U2: https://css4.pub/2015/textbook/somatosensory.pdf
_(note: маленький pdf)_

**[local-auto]** ERROR: unsupported/pdf

**[local-http]** ERROR: unsupported/pdf

**[local-curl]** ERROR: unsupported/pdf

**[local-browser]** ERROR: unsupported/pdf

**[firecrawl]** (3.83s, 7529 chars; wr=None, wo=None; hdr 3, code 0, links 0, lists 0)
```
# Anatomy of the Somatosensory System

FROM WIKIBOOKS<sup>1</sup>

Our somatosensory system consists of sensors in the skin
and sensors in our muscles, tendons, and joints. The receptors in the skin, the so called cutaneous receptors, tell
us about temperature (*thermoreceptors),* pressure and surface texture (*mechano receptors),* and pain (*nociceptors).*
The receptors in muscles and joints provide information
about muscle length, muscle tension, and joint angles.

## Cutaneous receptors

Sensory information from *Meissner corpuscles* and rapidly
adapting afferents leads to adjustment of grip force when
objects are lifted. These afferents respond with a brief
burst of action potentials when objects move a small distance during the early stages of lifting. In response to

Hairy skin Glabrous skin
Papillary Ridges
Epidermis
Free nerve Merkel ’s Septa
ending receptor
Meissne r’s
Sebaceous corpuscle
gland Dermis
Ruffini’s
 corpuscle
Hair receptor
Pacinian
corpuscle

This is a sample document to
showcase page-based formatting. It
contains a chapter from a Wikibook
called Sensory Systems. None of the
content has been changed in this
article, but some content has been
removed.

*Figure 1: Receptors in the human skin: Mechanoreceptors can
be free receptors or encapsulated.*
*Examples for free receptors are
the hair receptors at the roots of
hairs. Encapsulated receptors are
the Pacinian corpuscles and the
receptors in the glabrous (hairless) skin: Meissner corpuscles,*
*Ruffini corpuscles and Merkel’s
disks.*

1
The following description is based on lecture notes from Laszlo Zaborszky, from Rutgers University.

---

*Figure 2: Mammalian muscle
spindle showing typical position
in a muscle (left), neuronal connections in spinal cord (middle)
and expanded schematic (right).*
*Th

[…середина…]

rous surfaces, and at very low density in hairy skin.
This innervations density shrinks progressively with the
passage of time so that by the age of 50, the density in human digits is reduced to 10/mm<sup>2</sup>. Unlike rapidly adapting
axons, slowly adapting fibers respond not only to the initial indentation of skin, but also to sustained indentation
up to several seconds in duration.

Activation of the rapidly adapting *Pacinian corpuscles*
gives a feeling of vibration, while the slowly adapting
*Ruffini corpuscles* respond to the lataral movement or
stretching of skin.

## Nociceptors

Nociceptors have free nerve endings. Functionally, skin
nociceptors are either high-threshold mechanoreceptors

---

|  | Rapidly adapting | Slowly adapting |
| --- | --- | --- |
| Surface receptor / small receptive field | Hair receptor, Meissner's corpuscle: Detect an insect or a very fine vibration. Used for recognizing texture. | Merkel's receptor: Used for spatial details, e.g. a round surface edge or “an X” in brail. |
| Deep receptor / large receptive field | Pacinian corpuscle: “A diffuse vibration” e.g. tapping with a pencil. | Ruffini's corpuscle: “A skin stretch”. Used for joint positi
```

**[tavily]** (0.89s, 7277 chars; wr=None, wo=None; hdr 0, code 0, links 0, lists 0)
```
This is a sample document to showcase page-based formatting. It contains a chapter from a Wikibook called Sensory Systems. None of the content has been changed in this article, but some content has been removed.
Anatomy of the Somatosensory System FROM WIKIBOOKS1 Our somatosensory system consists of sensors in the skin and sensors in our muscles, tendons, and joints. The re-ceptors in the skin, the so called cutaneous receptors, tell us about temperature (thermoreceptors), pressure and sur-face texture (mechano receptors), and pain (nociceptors).
The receptors in muscles and joints provide information about muscle length, muscle tension, and joint angles.
Cutaneous receptors Sensory information from Meissner corpuscles and rapidly adapting afferents leads to adjustment of grip force when objects are lifted. These afferents respond with a brief burst of action potentials when objects move a small dis-tance during the early stages of lifting. In response to Figure 1: Receptors in the hu-man skin: Mechanoreceptors can be free receptors or encapsulated.
Examples for free receptors are the hair receptors at the roots of hairs. Encapsulated receptors are the Pacinian corpuscles and the receptors in the glabrous (hair-less) skin: Meissner corpuscles, Ruffini corpuscles and Merkel’s disks.
Hairy skin Glabrous skin Epidermis Dermis Pacinian corpuscle Papillary Ridges Septa Ruffini’s corpuscle Hair receptor Meissne r’s corpuscle Sebaceous gland Free nerve ending Merkel’s receptor 1 The following description is based on lecture notes from Laszlo Zaborszky, from Rutgers University.
1 Figure 2: Mammalian muscle spindle showing typical position in a muscle (left), neuronal con-nections in spinal cord (middle) and expanded schematic (right).
The spindle is a stretch receptor with its 

[…середина…]

sity shrinks progressively with the passage of time so that by the age of 50, the density in hu-man digits is reduced to 10/mm². Unlike rapidly adapting axons, slowly adapting fibers respond not only to the ini-tial indentation of skin, but also to sustained indentation up to several seconds in duration.
Activation of the rapidly adapting Pacinian corpuscles gives a feeling of vibration, while the slowly adapting Ruffini corpuscles respond to the lataral movement or stretching of skin.
Nociceptors Nociceptors have free nerve endings. Functionally, skin nociceptors are either high-threshold mechanoreceptors From Wikibooks 2 Rapidly adapting Slowly adapting Surface receptor / small receptive field Hair receptor, Meissner’s corpuscle: De-tect an insect or a very fine vibration.
Used for recognizing texture.
Merkel’s receptor: Used for spa-tial details, e.g. a round surface edge or “an X” in brail.
Deep receptor / large receptive field Pacinian corpuscle: “A diffuse vibra-tion” e.g. tapping with a pencil.
Ruffini’s corpuscle: “A skin stretch”. Used for joint position in fingers.
Table 1 Notice how figure captions and sidenotes are shown in the outside margin (on the left or right, depe
```

**[jina]** ERROR: {"error": "all fetch providers failed for https://css4.pub/2015/textbook/somatosensory.pdf: jina: jina network: [SSL: UN

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)

## U3: https://filesamples.com/samples/document/pdf/sample1.pdf
_(note: тестовый pdf)_

**[local-auto]** ERROR: unsupported/pdf

**[local-http]** ERROR: unsupported/pdf

**[local-curl]** ERROR: unsupported/pdf

**[local-browser]** ERROR: unsupported/pdf

**[firecrawl]** (2.02s, 10669 chars; wr=None, wo=None; hdr 7, code 0, links 0, lists 0)
```
# Instructions for Adding Your Logo & Address to AAO-HNSF Patient Handouts

# CO-BRANDING AAO-HNSF PATIENT HANDOUTS IS AS EASY AS 1-2-3!

## 1Download & Save Patient Handout

n Download the patient handout

You will need Adobe Acrobat Reader.
You can install it for free here:
**get.adobe.com/reader**

## n Save it to your computer

Remember where you save it; you will 
need to access it in the following steps.

PATIENT INFORMATION

Frequently Asked Questions: Earwax Prevention

QUESTION ANSWER

Should I do anything to my ears to prevent a buildup of earwax?

Your body makes earwax to protect your ear canal skin and protect it is most important to prevent lice on certain groups of people. Your health care provider with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with 

[…середина…]

g aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing aid, and with a physician may be helped are the safety people with hearing

**Your image** <u>must</u> **be saved as a .pdf file!**

## 2Upload Your
```

**[tavily]** (0.93s, 3000 chars; wr=None, wo=None; hdr 0, code 0, links 0, lists 0)
```
Instructions for Adding Your Logo & Address to AAO-HNSF Patient Handouts CO-BRANDING AAO-HNSF PATIENT HANDOUTS IS AS EASY AS 1-2-3!
Download & Save Patient Handout  Download the patient handout You will need Adobe Acrobat Reader.
You can install it for free here: get.adobe.com/reader  Save it to your computer Remember where you save it; you will need to access it in the following steps.
Upload Your Logo & Address Your image must be saved as a .pdf file! For additional information on how to save your logo/address as a .pdf file, please see the instructions below.
You will not be able to upload your personal information to the patient handout if the file is not saved in the .pdf format.
 Open the saved patient handout document  Click in the white space at the bottom of the page.  Within the Select Icon window, Browse to the .pdf file you would like to Insert and then click, OK.
The logo and/or address file will resize appropriately for the box.
 Type your web address in the blue rectangle below the white image field.
You’re Ready to Print!
 Save your file. Make sure to save your file before you close the document to ensure your logo and/ or address will be there the next time you open up the document.
 You are now ready to print!
Example of a co-branded Patient Handout: SAMPLE Click in this white space to upload your logo Click in this blue area to type your web address SAMPLE CONVERT YOUR LOGO TO .PDF Open a new Microsoft Word document. Remember where you save it; you will need to access it when uploading your logo/address to the Patient Handout.
Insert Your Image  Click the location in your Word document where you want to insert your image.
 Click the Insert tab, click Pictures.  Browse to the image you want to insert, select it, and then click Insert.
Your i
```

**[jina]** ERROR: {"error": "all fetch providers failed for https://filesamples.com/samples/document/pdf/sample1.pdf: jina: jina network: 

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)
