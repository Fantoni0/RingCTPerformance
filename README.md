# Ring Confidential Transaction Signatures Performance Analysis
Python implementation of the ring confidential transaction signatures used in [Monero](https://github.com/monero-project/monero).
More details about RingCT can be found [here](https://web.getmonero.org/library/Zero-to-Monero-2-0-0.pdf) on chapter 6.

We present a framework to analyze and compare the performance of ringCT using different elliptic curves.
The code is parallelized using `joblib` and it tries to run as many signatures in parallel as cpu cores available. 

:warning: This is a repository for research purposes. Cryptography is a pretty sensible issue and only reputed and tested sources should be used in a production environment. Use at your own risk!

:warning: Also bear in mind that Monero is a huge and dynamic open source project subjected to changes. The signatures here implemented might change in the future.

:information_source: The presented results were obtained using a Ryzen 7 3700X (16 cores) processor on Linux :penguin:. Times might change in different environments.

## Installation
Assuming that you have pip installed: 
```
git clone https://github.com/Fantoni0/RingCTPerformance
cd RingCTPerformance
pip install -r requirements.txt
```

### Requirements
The library has minimal requirements. All of them are included in requirements.txt.
Following the installation process solves the dependencies.
- `tinyec` for EC math.
- `nummaster` for modular square root.
- `matplotlib` for plotting the results.
- `joblib` for parallelization.

## Usage
An example of how to use the library:
```
python main.py -rs 8 16 32 64\ 
 -c brainpoolP160r1 secp192r1 secp224r1 secp256r1\
 -m 'I voted for Kodos'\ 
 -o comparative
```
If you want to experiment with single ring signatures, you can do so in `test_RingCT.ipynb`.
  
## Resources
Multiple ring signature algorithms exist and they might be confusing at first. Here are some pointers we found useful: 
* [Zero To Monero 2nd Edition](https://web.getmonero.org/library/Zero-to-Monero-2-0-0.pdf) - Great technical review of Monero
* [Mastering Monero](https://masteringmonero.com/free-download.html) - A complete guide about Monero and its ecosystem.
* Seminal and relevant papers about ring signatures.
    * [Group signatures](https://link.springer.com/content/pdf/10.1007/3-540-46416-6_22.pdf) - David Chaum - 1991
    * [How to leak a secret](https://link.springer.com/content/pdf/10.1007%252F3-540-45682-1_32.pdf) - Ronald L. Rivest, Adi Shamir and Yael Tauman - 2001
    * [Cryptonote Section 4](https://cryptonote.org/whitepaper.pdf) - Nicolas van Saberhagen - 2013
    * [Ring signature efficiency](https://bitcointalk.org/index.php?topic=972541.msg10619684#msg10619684) - Adam Black - 2015
    * Ring confidential transactions for Monero [[1]](https://www.researchgate.net/publication/311865049_Ring_Confidential_Transactions) [[2]](https://eprint.iacr.org/2015/1098.pdf) - Shen Noether and Adam Mackenzie - 2015

## Citation
This repository is part of a research article carried out by [ALFA](https://alfa.webs.upv.es/) research group. If you use it, please cite:
```
@article{larriba2021distributed,
  title={Distributed Trust, a Blockchain Election Scheme},
  author={Larriba, Antonio M and Cerd{\`a} i Cuc{\'o}, Aleix and Sempere, Jos{\'e} M and L{\'o}pez, Dami{\'a}n},
  journal={Informatica},
  volume={32},
  number={2},
  pages={321--355},
  year={2021},
  publisher={Vilnius University Institute of Data Science and Digital Technologies}
}
```


 


