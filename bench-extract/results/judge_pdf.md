# scenario: pdf

## U1: https://arxiv.org/pdf/1706.03762
_(note: Attention is all you need)_

**[local-auto]** ERROR: unsupported/pdf

**[local-http]** ERROR: unsupported/pdf

**[local-curl]** ERROR: unsupported/pdf

**[local-browser]** ERROR: network/

**[firecrawl]** (4.59s, 32000 chars; wr=None, wo=None; hdr 0, code 0, links 8, lists 0)
```
Provided proper attribution is provided, Google hereby grants permission to
reproduce the tables and figures in this paper solely for use in journalistic or
scholarly works.

Attention Is All You Need

∗ ∗ ∗ ∗
Ashish Vaswani Noam Shazeer Niki Parmar Jakob Uszkoreit
Google Brain Google Brain Google Research Google Research
[avaswani@google.com](mailto:avaswani@google.com) [noam@google.com](mailto:noam@google.com) [nikip@google.com](mailto:nikip@google.com) [usz@google.com](mailto:usz@google.com)

∗
Llion Jones
Google Research
[llion@google.com](mailto:llion@google.com)

∗ †
Aidan N. Gomez
University of Toronto
[aidan@cs.toronto.edu](mailto:aidan@cs.toronto.edu)

∗
Łukasz Kaiser
Google Brain
[lukaszkaiser@google.com](mailto:lukaszkaiser@google.com)

∗ ‡
Illia Polosukhin
[illia.polosukhin@gmail.com](mailto:illia.polosukhin@gmail.com)

Abstract

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
best

[…середина…]

1)} = \\cos \\left(p o s / 1 0 0 0 0 ^ {2 i / d \_ {\\mathrm {m o d e l}}}\\right)
$$

where pos is the position and i is the dimension. That is, each dimension of the positional encoding
corresponds to a sinusoid. The wavelengths form a geometric progression from 2π to 10000 · 2π. We
chose this function because we hypothesized it would allow the model to easily learn to attend by
relative positions, since for any fixed offset k, PEpos+kcan be represented as a linear function of
PEpos.
We also experimented with using learned positional embeddings \[9\] instead, and found that the two

$$
P E \_ {p o s + k}
$$

$$
P E \_ {p o s}
$$

We also experimented with using learned positional embeddings \[9\] instead, and found that the two
versions produced nearly identical results (see Table 3 row (E)). We chose the sinusoidal version
because it may allow the model to extrapolate to sequence lengths longer than the ones encountered
during training.

4 Why Self-Attention

In this section we compare various aspects of self-attention layers to the recurrent and convolutional layers commonly used for mapping one variable-length sequence of symbol representations
d
(x1,...,xn) to another sequenc
```

**[tavily]** (0.86s, 32000 chars; wr=None, wo=None; hdr 0, code 0, links 0, lists 0)
```
Provided proper attribution is provided, Google hereby grants permission to reproduce the tables and figures in this paper solely for use in journalistic or scholarly works.
Attention Is All You Need Ashish Vaswani∗ Google Brain avaswani@google.com Noam Shazeer∗ Google Brain noam@google.com Niki Parmar∗ Google Research nikip@google.com Jakob Uszkoreit∗ Google Research usz@google.com Llion Jones∗ Google Research llion@google.com Aidan N. Gomez∗† University of Toronto aidan@cs.toronto.edu Łukasz Kaiser∗ Google Brain lukaszkaiser@google.com Illia Polosukhin∗‡ illia.polosukhin@gmail.com Abstract The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.
∗Equal contribution. Listing order is random. Jakob proposed 

[…середина…]

tention O(n2 · d) O(1) O(1) Recurrent O(n · d2) O(n) O(n) Convolutional O(k · n · d2) O(1) O(logk(n)) Self-Attention (restricted) O(r · n · d) O(1) O(n/r) 3.5 Positional Encoding Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence. To this end, we add "positional encodings" to the input embeddings at the bottoms of the encoder and decoder stacks. The positional encodings have the same dimension dmodel as the embeddings, so that the two can be summed. There are many choices of positional encodings, learned and fixed [9].
In this work, we use sine and cosine functions of different frequencies: PE(pos,2i) = sin(pos/100002i/dmodel) PE(pos,2i+1) = cos(pos/100002i/dmodel) where pos is the position and i is the dimension. That is, each dimension of the positional encoding corresponds to a sinusoid. The wavelengths form a geometric progression from 2π to 10000 · 2π. We chose this function because we hypothesized it would allow the model to easily learn to attend by relative positions, since for any fixed offset k, PEpo
```

**[jina]** (0.86s, 32000 chars; wr=None, wo=None; hdr 4, code 0, links 0, lists 0)
```
Title: 1706.03762v7.pdf

URL Source: https://arxiv.org/pdf/1706.03762

Published Time: Fri, 12 Apr 2024 23:47:34 GMT

Number of Pages: 15

Markdown Content:
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

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We s

[…середина…]

imum path lengths, per-layer complexity and minimum number of sequential operations for different layer types. n is the sequence length, d is the representation dimension, k is the kernel size of convolutions and r the size of the neighborhood in restricted self-attention. Layer Type Complexity per Layer Sequential Maximum Path Length Operations Self-Attention O(n2 · d) O(1) O(1) 

Recurrent O(n · d2) O(n) O(n)

Convolutional O(k · n · d2) O(1) O(log k(n)) 

Self-Attention (restricted) O(r · n · d) O(1) O(n/r )

3.5 Positional Encoding 

Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence. To this end, we add "positional encodings" to the input embeddings at the bottoms of the encoder and decoder stacks. The positional encodings have the same dimension dmodel 

as the embeddings, so that the two can be summed. There are many choices of positional encodings, learned and fixed [9]. In this work, we use sine and cosine functions of different frequencies: 

P E (pos, 2i) = sin (pos/ 10000 2i/d model )

P E (pos, 2i
```

**[parallel]** (2.49s, 14753 chars; wr=None, wo=None; hdr 1, code 0, links 0, lists 0)
```
Provided proper attribution is provided, Google hereby grants permission to reproduce the tables and figures in this paper solely for use in journalistic or scholarly works.

...

# arXiv:1706.03762v7 [cs.CL] 2 Aug 2023
**1 Introduction**

...

Numerous efforts have since continued to push the boundaries of recurrent language models and encoder-decoder architectures [38, 24, 15].

...

This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths, as memory constraints limit batching across examples.
Recent work has achieved significant improvements in computational efficiency through factorization tricks [21] and conditional computation [32], while also improving model performance in case of the latter. The fundamental constraint of sequential computation, however, remains.
Attention mechanisms have become an integral part of compelling sequence modeling and transduc- tion models in various tasks, allowing modeling of dependencies without regard to their distance in the input or output sequences [2, 19].
In all but a few cases [27], however, such attention mechanisms are used in conjunction with a recurrent network.
In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output.
The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs.
**2 Background**

...

In the Transformer this is reduced to a constant number of operations, albeit at the cost of reduced effective resolution due to averaging attention-weighted positions, an effect we co

[…середина…]

d_ model _/h_ = 64. Due to the reduced dimension of each head, the total computational cost is similar to that of single-head attention with full dimensionality.
**3.2.3 Applications of Attention in our Model**
The Transformer uses multi-head attention in three different ways:
• In "encoder-decoder attention" layers, the queries come from the previous decoder layer, and the memory keys and values come from the output of the encoder. This allows every position in the decoder to attend over all positions in the input sequence.
This mimics the typical encoder-decoder attention mechanisms in sequence-to-sequence models such as [38, 2, 9].

...

• Similarly, self-attention layers in the decoder allow each position in the decoder to attend to all positions in the decoder up to and including that position. We need to prevent leftward information flow in the decoder to preserve the auto-regressive property.
We implement this inside of scaled dot-product attention by masking out (setting to _−∞_ ) all values in the input of the softmax which correspond to illegal connections. See Figure 2.
**3.3 Position-wise Feed-Forward Networks**
In addition to attention sub-layers, each of the layers in
```

## U2: https://css4.pub/2015/textbook/somatosensory.pdf
_(note: маленький pdf)_

**[local-auto]** ERROR: unsupported/pdf

**[local-http]** ERROR: unsupported/pdf

**[local-curl]** ERROR: unsupported/pdf

**[local-browser]** ERROR: unsupported/pdf

**[firecrawl]** (4.79s, 6582 chars; wr=None, wo=None; hdr 0, code 0, links 0, lists 0)
```
Anatomy of the Somatosensory System

1
FROM WIKIBOOKS

Our somatosensory system consists of sensors in the skin
and sensors in our muscles, tendons, and joints. The receptors in the skin, the so called cutaneous receptors, tell
us about temperature (thermoreceptors), pressure and surface texture (mechano receptors), and pain (nociceptors).
The receptors in muscles and joints provide information
about muscle length, muscle tension, and joint angles.

Our somatosensory system consists of sensors in the skin
and sensors in our muscles, tendons, and joints. The receptors in the skin, the so called cutaneous receptors, tell
us about temperature (thermoreceptors), pressure and surface texture (mechano receptors), and pain (nociceptors).
The receptors in muscles and joints provide information
about muscle length, muscle tension, and joint angles.

Cutaneous receptors

Sensory information from Meissner corpuscles and rapidly
adapting afferents leads to adjustment of grip force when
objects are lifted. These afferents respond with a brief
burst of action potentials when objects move a small distance during the early stages of lifting. In response to

This is a sample document to
showcase page-based formatting. It
contains a chapter from a Wikibook
called Sensory Systems. None of the
content has been changed in this
article, but some content has been
removed.

Figure 1: Receptors in the human skin: Mechanoreceptors can
be free receptors or encapsulated.
Examples for free receptors are
the hair receptors at the roots of
hairs. Encapsulated receptors are
the Pacinian corpuscles and the
receptors in the glabrous (hairless) skin: Meissner corpuscles,
Ruffini corpuscles and Merkel’s
disks.

1
The following description is based on lecture notes from Laszlo Zaborszky, from Rutgers Unive

[…середина…]

 increases
reflexively until the gripped object no longer moves. Such
a rapid response to a tactile stimulus is a clear indication
of the role played by somatosensory neurons in motor activity.
The slowly adapting Merkel’s receptors are responsible

The slowly adapting Merkel’s receptors are responsible
for form and texture perception. As would be expected for
receptors mediating form perception, Merkel’s receptors
are present at high density in the digits and around the
mouth (50/mm² of skin surface), at lower density in other glabrous surfaces, and at very low density in hairy skin.
This innervations density shrinks progressively with the
passage of time so that by the age of 50, the density in human digits is reduced to 10/mm². Unlike rapidly adapting
axons, slowly adapting fibers respond not only to the initial indentation of skin, but also to sustained indentation
up to several seconds in duration.
Activation of the rapidly adapting Pacinian corpuscles

Nociceptors

Activation of the rapidly adapting Pacinian corpuscles
gives a feeling of vibration, while the slowly adapting
Ruffini corpuscles respond to the lataral movement or
stretching of skin.

---

|  | Rapidly adapting |
```

**[tavily]** (0.74s, 7277 chars; wr=None, wo=None; hdr 0, code 0, links 0, lists 0)
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

**[jina]** (2.94s, 7552 chars; wr=None, wo=None; hdr 1, code 0, links 0, lists 0)
```
Title: Anatomy of the Somatosensory System

URL Source: https://css4.pub/2015/textbook/somatosensory.pdf

Published Time: Wed, 25 Mar 2015 13:22:12 GMT

Number of Pages: 4

Markdown Content:
This is a sample document to showcase page-based formatting. It contains a chapter from a Wikibook called Sensory Systems. None of the content has been changed in this article, but some content has been removed. 

# Anatomy of the Somatosensory System 

FROM WIKIBOOKS 1

Our somatosensory system consists of sensors in the skin and sensors in our muscles, tendons, and joints. The re-ceptors in the skin, the so called cutaneous receptors, tell us about temperature ( thermoreceptors ), pressure and sur-face texture ( mechano receptors ), and pain ( nociceptors ). The receptors in muscles and joints provide information about muscle length, muscle tension, and joint angles. 

Cutaneous receptors 

Sensory information from Meissner corpuscles and rapidly adapting afferents leads to adjustment of grip force when objects are lifted. These afferents respond with a brief burst of action potentials when objects move a small dis-tance during the early stages of lifting. In response to 

Figure 1: Receptors in the hu-man skin: Mechanoreceptors can be free receptors or encapsulated. Examples for free receptors are the hair receptors at the roots of hairs. Encapsulated receptors are the Pacinian corpuscles and the receptors in the glabrous (hair-less) skin: Meissner corpuscles, Ruffini corpuscles and Merkel’s disks. 

Hairy skin Glabrous skin Epidermis Dermis  

> Pacinian corpuscle Papillary Ridges Septa Ruffini’s corpuscle Hair receptor Meissne r’s corpuscle Sebaceous gland Free nerve ending Merkel ’s receptor

1 The following description is based on lecture notes from Laszlo Zaborszky, from Rut

[…середина…]

th-er glabrous surfaces, and at very low density in hairy skin. This innervations density shrinks progressively with the passage of time so that by the age of 50, the density in hu-man digits is reduced to 10/mm². Unlike rapidly adapting axons, slowly adapting fibers respond not only to the ini-tial indentation of skin, but also to sustained indentation up to several seconds in duration. Activation of the rapidly adapting Pacinian corpuscles 

gives a feeling of vibration, while the slowly adapting 

Ruffini corpuscles respond to the lataral movement or stretching of skin. 

Nociceptors 

Nociceptors have free nerve endings. Functionally, skin nociceptors are either high-threshold mechanoreceptors 

From Wikibooks 2Rapidly adapting Slowly adapting 

Surface receptor / small receptive field 

Hair receptor , Meissner’s corpuscle : De-tect an insect or a very fine vibration. Used for recognizing texture. Merkel’s receptor: Used for spa-tial details, e.g. a round surface edge or “an X” in brail. Deep receptor / large receptive field 

Pacinian corpuscle : “A diffuse vibra-tion” e.g. tapping with a pencil. 

Ruffini’s corpuscle : “A skin stretch”. Used for joint position in fingers. 


```

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)

## U3: https://filesamples.com/samples/document/pdf/sample1.pdf
_(note: тестовый pdf)_

**[local-auto]** ERROR: unsupported/pdf

**[local-http]** ERROR: unsupported/pdf

**[local-curl]** ERROR: unsupported/pdf

**[local-browser]** ERROR: unsupported/pdf

**[firecrawl]** (2.64s, 10669 chars; wr=None, wo=None; hdr 7, code 0, links 0, lists 0)
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

**[tavily]** (0.71s, 3000 chars; wr=None, wo=None; hdr 0, code 0, links 0, lists 0)
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

**[jina]** (1.76s, 3379 chars; wr=None, wo=None; hdr 1, code 0, links 0, lists 0)
```
Title: sample1.pdf

URL Source: https://filesamples.com/samples/document/pdf/sample1.pdf

Published Time: Wed, 05 Jul 2023 18:52:49 GMT

Number of Pages: 1

Markdown Content:
Instructions for Adding Your Logo & Address to AAO-HNSF Patient Handouts 

CO-BRANDING AAO-HNSF PATIENT HANDOUTS IS AS EASY AS 1-2-3! 

Download & Save Patient Handout 

 Download the patient handout 

You will need Adobe Acrobat Reader. 

You can install it for free here: 

get.adobe.com/reader 

 Save it to your computer 

Remember where you save it; you will 

need to access it in the following steps. 

Upload Your Logo & Address 

Your image  must  be saved as a .pdf file! 

For additional information on how to 

save your logo/address as a .pdf file, 

please see the instructions below. 

You will not be able to upload your personal 

information to the patient handout if the file 

is not saved in the .pdf format. 

 Open the saved patient handout document 

 Click in the white space at the bottom of 

the page. 

 Within the  Select Icon  window, 

Browse  to the .pdf file you would 

like to  Insert  and then click,  OK .

The logo and/or address file will resize 

appropriately for the box. 

 Type your web address in the blue 

rectangle below the white image field. 

You’re Ready to Print! 

 Save your file. 

Make sure to save your file before you close 

the document to ensure your logo and/ 

or address will be there the next time you 

open up the document. 

 You are now ready to print! 

Example of a co-branded Patient Handout: 

> S A M P L E

Click in this white space to upload your logo 

Click in this blue area to type your web address 

> S A M P L E

CONVERT YOUR LOGO TO .PDF 

Open a new Microsoft Word document. 

Remember where you save it; you will need to access i
```

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)
