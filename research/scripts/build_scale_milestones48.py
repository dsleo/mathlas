#!/usr/bin/env python3
"""Direct primary-source milestone pass for scale batch 48."""
import json
from pathlib import Path
from build_scale_milestones49 import a,d,x,ms,person
from build_pilot_milestones2 import m
BASE=Path(__file__).resolve().parents[1]/'data/collection/enrichment/scale'

taubes=a('math/0611007','The Seiberg-Witten equations and the Weinstein conjecture',2006,'C. H. Taubes')
hutch=a('0809.0140','The Weinstein conjecture for stable Hamiltonian structures',2008,'M. Hutchings and C. H. Taubes')
ech=a('1003.3209','Embedded contact homology and its applications',2010,'M. Hutchings')
kw=a('hep-th/0604151','Electric-Magnetic Duality And The Geometric Langlands Program',2006,'A. Kapustin and E. Witten')
kwpub=d('10.4310/CNTP.2007.v1.n1.a1','Electric-Magnetic Duality And The Geometric Langlands Program',2007,'A. Kapustin and E. Witten')
bg=d('10.4007/annals.2008.167.625','Uniform expansion bounds for Cayley graphs of SL2(Fp)',2008,'J. Bourgain and A. Gamburd')
aff=d('10.1007/s00222-009-0225-3','Affine linear sieve, expanders, and sum-product',2009,'J. Bourgain, A. Gamburd and P. Sarnak')
aff2=a('0912.5021',"Generalization of Selberg's 3/16 Theorem and Affine Sieve",2009,'J. Bourgain, A. Gamburd and P. Sarnak')
aw=a('0709.0248','Homotopy theoretic models of identity types',2007,'S. Awodey and M. Warren')
voev=x('https://www.math.ias.edu/vladimir/sites/math.ias.edu.vladimir/files/univalent_foundations_project.pdf','Univalent Foundations Project',2010,'V. Voevodsky','Voevodsky / Institute for Advanced Study')
ias=x('https://www.ias.edu/math/sp/univalent','Special Year 2012–13: Univalent Foundations of Mathematics',2012,'Institute for Advanced Study','Institute for Advanced Study')
hott=a('1308.0729','Homotopy Type Theory: Univalent Foundations of Mathematics',2013,'The Univalent Foundations Program')
baker=a('math/0701075','Specialization of linear systems from curves to graphs',2007,'M. Baker')
jr=a('1701.06579','Brill-Noether theory for curves of a fixed gonality',2017,'D. Jensen and D. Ranganathan')
jp=a('1808.01285','On the strong maximal rank conjecture in genus 22 and 23',2018,'D. Jensen and S. Payne')
eo=a('math-ph/0702045','Invariants of algebraic curves and topological expansion',2007,'B. Eynard and N. Orantin')
wp=a('0705.3600',"Weil-Petersson volume of moduli spaces, Mirzakhani's recursion and matrix models",2007,'B. Eynard and N. Orantin')
bkmp=a('1205.1103','Computation of open Gromov-Witten invariants for toric Calabi-Yau 3-folds by topological recursion, a proof of the BKMP conjecture',2012,'B. Eynard and N. Orantin')
flag=d('10.2178/jsl/1203350785','Flag algebras',2007,'A. A. Razborov')
flagguide=a('1607.04741','Flag Algebras: A First Glance',2016,'M. K. de Carli Silva, F. M. de Oliveira Filho and C. M. Sato')
gk=a('1011.4105','On the Erdos distinct distance problem in the plane',2010,'L. Guth and N. H. Katz')
gkpub=d('10.4007/annals.2015.181.1.2','On the Erdős distinct distances problem in the plane',2015,'L. Guth and N. H. Katz')
lqg=a('0808.1560','Liouville Quantum Gravity and KPZ',2008,'B. Duplantier and S. Sheffield')
mate=a('1409.7055','Liouville quantum gravity as a mating of trees',2014,'B. Duplantier, J. Miller and S. Sheffield')
ksdev=a('1303.3253','Wall-crossing structures in Donaldson-Thomas invariants, integrable systems and Mirror Symmetry',2013,'M. Kontsevich and Y. Soibelman')
ks=a('0811.2435','Stability structures, motivic Donaldson-Thomas invariants and cluster transformations',2008,'M. Kontsevich and Y. Soibelman')

spec={
'QC73':{'canonicalName':'Seiberg–Witten theory and embedded contact homology prove Weinstein-type Reeb dynamics','aliases':['Weinstein conjecture','embedded contact homology','Seiberg-Witten Floer homology','Reeb orbit'], 'milestones':[
 ms('first_statement',taubes,'Seiberg–Witten proof of Weinstein posted','Taubes presents the three-dimensional closed-Reeb-orbit theorem using gauge-theoretic methods.',['Clifford Taubes'],note='The same work both states and proves the target result.'),
 ms('first_application',taubes,'Gauge theory proves closed Reeb orbit','The Seiberg–Witten equations are used intentionally to prove the Weinstein conjecture in dimension three.',['Clifford Taubes'],note='The same work serves both first-statement and first-application roles.'),
 ms('key_development',hutch,'ECH–Seiberg–Witten bridge strengthens Weinstein results','Hutchings and Taubes apply the ECH/Floer equivalence to stable Hamiltonian structures.',['Michael Hutchings','Clifford Taubes']),
 ms('consolidation',ech,'Embedded contact homology survey','Hutchings surveys the Floer-theoretic bridge and Reeb-dynamics applications.',['Michael Hutchings'])],
 'people':[person('Clifford Taubes','developer','https://en.wikipedia.org/wiki/Clifford_Taubes',taubes,'Proves the 3D Weinstein conjecture')],
 'notes':'Catalogue name mentions exotic spheres, smooth Poincaré in dimension four and Heegaard Floer, none of which describes the supplied summary. This record follows the event summary (Weinstein via gauge theory/ECH); the canonical name needs editorial correction. The 2006 preprint predates the 2007 journal issue.'},
'QC31':{'aliases':['Kapustin-Witten correspondence','geometric Langlands and S-duality','electric-magnetic duality','Hecke eigensheaves from branes'], 'milestones':[
 ms('first_statement',kw,'Geometric Langlands interpreted via S-duality','The 2006 public preprint sets out the N=4 gauge-theory interpretation.',['Anton Kapustin','Edward Witten'],note='The same work also carries out the proposed dictionary.'),
 ms('first_application',kw,'Branes yield Hecke-eigensheaf dictionary','The paper applies electric–magnetic duality and brane constructions to objects of geometric Langlands.',['Anton Kapustin','Edward Witten'],note='The same work serves both formulation and application roles.'),
 ms('key_development',kwpub,'Kapustin–Witten paper published','The peer-reviewed version appeared in 2007.',['Anton Kapustin','Edward Witten'])],
 'people':[person('Edward Witten','developer','https://en.wikipedia.org/wiki/Edward_Witten',kw,'Co-develops the gauge-theoretic Langlands dictionary')],
 'notes':'The 2024 proof of geometric Langlands is a different mathematical result and is not claimed to validate each physics derivation. The 2006 preprint governs the public date; no event-specific institution verified.'},
'P27':{'aliases':['affine sieve','thin groups','expander sieve','sum-product theorem'], 'milestones':[
 ms('precursor',bg,'Cayley-graph expansion for SL2','Expansion estimates prepare the sieve transfer.',['Jean Bourgain','Alex Gamburd']),
 ms('first_statement',aff,'Affine sieve paper published online','The publisher dates the first online publication 26 November 2009; the issue is March 2010.',['Jean Bourgain','Alex Gamburd','Peter Sarnak'],note='The same paper both formulates and applies the sieve.'),
 ms('first_application',aff,'Expansion and sum-product sieve thin orbits','The paper applies expander bounds to almost-prime values along affine orbits.',['Jean Bourgain','Alex Gamburd','Peter Sarnak'],note='The same paper serves both statement and application roles.'),
 ms('key_development',aff2,'Affine sieve strengthened through spectral gap','A companion preprint gives sharp sieve upper bounds using a different orbit ordering.',['Jean Bourgain','Alex Gamburd','Peter Sarnak'])],
 'people':[person('Peter Sarnak','developer','https://en.wikipedia.org/wiki/Peter_Sarnak',aff,'Co-develops affine sieve for thin-orbit problems')],
 'notes':'The 2008 received date is not a public publication date. The checked publisher gives online 2009 and journal issue 2010; no earlier public manuscript date was verified. The later companion was posted in December 2009.'},
'Q52':{'aliases':['homotopy type theory','HoTT','univalence axiom','univalent foundations','UniMath'], 'milestones':[
 ms('precursor',aw,'Homotopy models of identity types','The 2007 paper connects type-theoretic identity with homotopy models.',['Steve Awodey']),
 ms('first_statement',voev,'Voevodsky posts univalent-foundations project','A dated 2010 author document explains univalent semantics and the univalence axiom.',['Vladimir Voevodsky'],kind='primary_text',note='The 2005 private conception and 2009 talks are discussed as antecedents, not substituted for a public document.'),
 ms('first_application',voev,'Univalent foundations formalized in Coq','The 2010 document describes and links Coq files containing definitions and basic proofs.',['Vladimir Voevodsky'],kind='primary_text',note='The same public document serves both statement and first documented application roles.'),
 ms('institution',ias,'IAS Special Year on Univalent Foundations begins','A named 2012–13 research programme gathers the community.',['Vladimir Voevodsky'],kind='primary_text'),
 ms('consolidation',hott,'Homotopy Type Theory book published','The 2013 collective book systematically presents univalent foundations and examples.',['The Univalent Foundations Program'])],
 'people':[person('Steve Awodey','developer','https://en.wikipedia.org/wiki/Steve_Awodey',aw,'Develops homotopy-theoretic identity models')],
 'notes':'Voevodsky reports earlier ideas and 2009–10 talks, but the dated 2010 public project document is the conservative first-statement anchor here. The 2012–13 IAS programme and 2013 HoTT book are distinct institutional and consolidation milestones.'},
'Q71':{'aliases':['tropical Brill-Noether theory','chip firing on graphs','linear systems on metric graphs','strong maximal rank'], 'milestones':[
 ms('first_statement',baker,'Specialization from curves to graphs','Baker formulates the tropical specialization method for linear systems.',['Matthew Baker'],note='The same paper applies it to curve theory.'),
 ms('first_application',baker,'Graph divisors constrain algebraic-curve linear series','The paper uses specialization to transfer divisor-rank information to curves.',['Matthew Baker'],note='The same work serves both first-statement and first-application roles.'),
 ms('key_development',jr,'Fixed-gonality Brill–Noether theorem','Jensen and Ranganathan use tropical divisor theory and logarithmic maps.',['David Jensen','Dhruv Ranganathan']),
 ms('key_development',jp,'Tropical methods reach maximal rank cases','Tropicalized linear series prove two cases of the strong maximal rank conjecture.',['David Jensen','Sam Payne'])],
 'people':[person('Matthew Baker','originator','https://en.wikipedia.org/wiki/Matthew_Baker_(mathematician)',baker,'Introduces curve-to-graph specialization')],
 'notes':'The 2018 paper explicitly revised a claimed consequence about moduli spaces after finding a gap; only its retained maximal-rank theorem is recorded. Searched the cited arXiv records for a field-naming institution; none verified.'},
'QC52':{'aliases':['Eynard-Orantin topological recursion','matrix-model recursion','Weil-Petersson volumes','BKMP conjecture'], 'milestones':[
 ms('first_statement',eo,'Eynard–Orantin recursion formulated','The 2007 preprint defines algebraic-curve invariants and recursive topological expansion.',['Bertrand Eynard','Nicolas Orantin']),
 ms('first_application',eo,'Recursion applied to Kontsevich integral','The founding paper applies its invariants to the Kontsevich integral and gives a KdV result.',['Bertrand Eynard','Nicolas Orantin'],note='The same paper serves both definition and first-application roles.'),
 ms('key_development',wp,'Recursion applied to Weil–Petersson volumes','A later 2007 paper identifies Mirzakhani volume recursion with matrix-model loop equations.',['Bertrand Eynard','Nicolas Orantin']),
 ms('key_development',bkmp,'Topological recursion proves BKMP conjecture','The method computes toric Calabi–Yau open Gromov–Witten invariants in general.',['Bertrand Eynard','Nicolas Orantin'])],
 'people':[person('Nicolas Orantin','originator','https://en.wikipedia.org/wiki/Nicolas_Orantin',eo,'Co-defines topological recursion')],
 'notes':'The founding February 2007 preprint already applies the method to the Kontsevich integral; the May 2007 Weil–Petersson paper is a further application. No earlier event-specific institution found from the cited records.'},
'WC100':{'aliases':['flag algebras','Razborov flag algebra method','semidefinite extremal combinatorics','graph homomorphism densities'], 'milestones':[
 ms('first_statement',flag,'Razborov introduces flag algebras','The 2007 Journal of Symbolic Logic paper defines the algebraic framework.',['Alexander Razborov'],note='The same paper defines, names and uses the method.'),
 ms('first_application',flag,'Flag algebras applied to extremal graph bounds','The founding paper obtains graph-density inequalities through the framework.',['Alexander Razborov'],note='The same paper serves both statement and application roles.'),
 ms('naming',flag,'Flag algebras named in article title','The 2007 title gives a reproducible naming anchor.',['Alexander Razborov'],note='The same work both defines and names the field.'),
 ms('consolidation',flagguide,'Introductory flag-algebra survey','A later guide explains computer-assisted extremal proofs.',['Alexander Razborov'])],
 'people':[person('Alexander Razborov','originator','https://en.wikipedia.org/wiki/Alexander_Razborov',flag,'Introduces flag algebras')],
 'notes':'The founding journal issue is December 2007. A metadata service may show DOI processing in 2008; the publisher issue supplies the stated year.'},
'WC66/QC23':{'aliases':['Guth-Katz distinct distances','Erdős distinct distances problem','polynomial partitioning','Elekes-Sharir framework'], 'milestones':[
 ms('first_statement',gk,'Guth–Katz distinct-distances preprint','The 2010 paper announces the near-sharp planar distance bound.',['Larry Guth','Nets Katz'],note='The same work proves the target theorem.'),
 ms('first_application',gk,'Polynomial incidence geometry bounds distances','Polynomial partitioning and ruled-surface geometry are applied to the Erdős distance problem.',['Larry Guth','Nets Katz'],note='The same paper serves both statement and target-application roles.'),
 ms('key_development',gkpub,'Distinct-distances proof appears in Annals','The 2015 journal publication supplies a later formal record.',['Larry Guth','Nets Katz'])],
 'people':[person('Larry Guth','developer','https://en.wikipedia.org/wiki/Larry_Guth',gk,'Co-proves near-sharp distinct-distance bound')],
 'notes':'The 2010 public preprint, not the 2015 Annals issue, sets the first public date. No separately named institution for this particular transfer was verified.'},
'QC60':{'aliases':['Liouville quantum gravity','mating of trees','peanosphere','quantum zipper','SLE'], 'milestones':[
 ms('precursor',lqg,'Probabilistic LQG and KPZ relation','The 2008 work constructs a Gaussian-free-field LQG measure and KPZ interpretation.',[],phase='probabilistic LQG'),
 ms('first_statement',mate,'Mating-of-trees LQG construction posted','The 2014 preprint canonically embeds a pair of continuum random trees as an LQG sphere.',['Bertrand Duplantier','Jason Miller','Scott Sheffield'],phase='mating of trees',note='The same work applies the construction to SLE-decorated maps.'),
 ms('first_application',mate,'Tree mating identifies SLE-decorated LQG','The paper relates the continuum tree pair to SLE and decorated random-planar-map scaling limits.',['Bertrand Duplantier','Jason Miller','Scott Sheffield'],phase='mating of trees',note='The same paper serves both statement and first-application roles.')],
 'people':[person('Scott Sheffield','developer','https://en.wikipedia.org/wiki/Scott_Sheffield',mate,'Co-develops the mating-of-trees construction')],
 'phases':['probabilistic LQG','mating of trees'],
 'notes':'The 2008 probabilistic LQG paper predates the 2014 mating-of-trees construction; this event is specifically the latter bridge. No event-specific named institution verified.'},
'WC110':{'aliases':['Kontsevich–Soibelman wall crossing','motivic Donaldson–Thomas invariants','stability structures','cluster transformations'], 'milestones':[
 ms('first_statement',ks,'Motivic DT wall-crossing framework posted','Kontsevich and Soibelman define stability structures and motivic invariants in 2008.',['Maxim Kontsevich','Yan Soibelman'],note='The same paper develops and applies wall-crossing identities.'),
 ms('first_application',ks,'Wall-crossing relates DT and cluster transformations','The founding work applies its identities to 3-Calabi–Yau categories and cluster collections.',['Maxim Kontsevich','Yan Soibelman'],note='The same work serves both statement and first-application roles.'),
 ms('key_development',ksdev,'Wall-crossing structures extended','The 2013 paper develops wall-crossing structures in DT invariants and integrable systems.',['Maxim Kontsevich','Yan Soibelman'])],
 'people':[person('Yan Soibelman','originator','https://en.wikipedia.org/wiki/Yan_Soibelman',ks,'Co-develops motivic wall-crossing formula')],
 'notes':'This 2008 preprint is the specific Kontsevich–Soibelman framework, not the first use of wall-crossing generally. No defensible first field-naming or institutional anchor was established from the cited records.'}
}

def main():
 rows=[]
 for e in json.loads((BASE/'batch48.json').read_text()):
  s=spec[e['eventId']]
  rows.append({'pid':e['pid'],'eventId':e['eventId'],'canonicalName':s.get('canonicalName',e['name']),'aliases':s['aliases'],'phases':s.get('phases',[]),'milestones':sorted(s['milestones'],key=lambda t:t['year']),'people':s['people'],'notes':s['notes']})
 (BASE/'milestones48.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 print(len(rows),sum(len(r['milestones']) for r in rows))
if __name__=='__main__':main()
