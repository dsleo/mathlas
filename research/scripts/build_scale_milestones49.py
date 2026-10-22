#!/usr/bin/env python3
"""Source-led milestone records for scale batch 49; URLs are primary records."""
import json
from pathlib import Path
from build_pilot_milestones2 import m

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/collection/enrichment/scale'

def a(id, title, year, authors):
    return {'url': 'https://arxiv.org/abs/' + id, 'title': title, 'year': year, 'authors': authors, 'source': 'arXiv'}
def d(doi, title, year, authors):
    return {'url': 'https://doi.org/' + doi, 'title': title, 'year': year, 'authors': authors, 'source': 'publisher / Crossref'}
def x(url, title, year, authors, source):
    return {'url': url, 'title': title, 'year': year, 'authors': authors, 'source': source}
def ms(role, rec, label, description, people, *, note=None, phase=None, kind='bibliographic_record'):
    work = f"{rec['authors']}, {rec['title']} ({rec['year']})" if kind == 'bibliographic_record' else None
    return m(role, rec['year'], label, work, people, description,
             [{'claim': f"The source documents {label.lower()} in {rec['year']}", 'source': rec['source'], 'url': rec['url'], 'kind': kind}], note=note, phase=phase)
def person(name, role, url, rec, why):
    return {'name': name, 'role': role, 'lifespan': None, 'biographyUrl': url,
            'works': [{'citation': f"{rec['authors']}, {rec['title']}", 'year': rec['year'], 'url': rec['url'], 'whyItMatters': why}]}

wise=x('https://www.math.mcgill.ca/wise/papers.htm','The Structure of Groups with a Quasiconvex Hierarchy',2011,'D. T. Wise','Wise publication list')
agol=a('1204.2810','The virtual Haken conjecture',2012,'I. Agol')
agolpub=d('10.4171/dm/421','The virtual Haken conjecture',2013,'I. Agol')
sak=a('1203.0039','Periods and harmonic analysis on spherical varieties',2012,'Y. Sakellaridis and A. Venkatesh')
gw=a('0807.3720','S-Duality of Boundary Conditions In N=4 Super Yang-Mills Theory',2008,'D. Gaiotto and E. Witten')
bzsv23=x('https://www.math.ias.edu/~akshay/research/BZSVpaperV1.pdf','Relative Langlands duality, first publicly circulated draft',2023,'D. Ben-Zvi, Y. Sakellaridis and A. Venkatesh','Venkatesh author site / first draft')
bzsv24=a('2409.04677','Relative Langlands Duality',2024,'D. Ben-Zvi, Y. Sakellaridis and A. Venkatesh')
ober=d('10.4171/OWR/2025/18','Arbeitsgemeinschaft: Relative Langlands Duality',2025,'D. Ben-Zvi, Y. Sakellaridis and A. Venkatesh')
fr1=a('2304.02678','Friedman-Ramanujan functions in random hyperbolic geometry and application to spectral gaps I',2023,'N. Anantharaman and L. Monk')
tangle=a('2401.01601','A Moebius inversion formula to discard tangled hyperbolic surfaces',2024,'N. Anantharaman and L. Monk')
fr2=a('2502.12268','Friedman-Ramanujan functions in random hyperbolic geometry and application to spectral gaps II',2025,'N. Anantharaman and L. Monk')
ten=a('math/0503363','The Ten Martini Problem',2005,'A. Avila and S. Jitomirskaya')
avila=a('0905.3902','Global theory of one-frequency Schrodinger operators I: stratified analyticity of the Lyapunov exponent and the boundary of nonuniform hyperbolicity',2009,'A. Avila')
avilapub=d('10.1007/s11511-015-0128-7','Global theory of one-frequency Schrödinger operators',2015,'A. Avila')
hr=a('0909.2190','Stable group theory and approximate subgroups',2009,'E. Hrushovski')
bgt=a('1110.5008','The structure of approximate groups',2011,'E. Breuillard, B. Green and T. Tao')
pos=a('1212.5605','Scattering Amplitudes and the Positive Grassmannian',2012,'N. Arkani-Hamed et al.')
amp=a('1312.2007','The Amplituhedron',2013,'N. Arkani-Hamed and J. Trnka')
prime=a('math/0606088','Linear Equations in Primes',2006,'B. Green and T. Tao')
mob=a('0807.1736','The Mobius function is strongly orthogonal to nilsequences',2008,'B. Green and T. Tao')
invann=a('1006.0205','An inverse theorem for the Gowers U^{s+1}[N]-norm (announcement)',2010,'B. Green, T. Tao and T. Ziegler')
inv=a('1009.3998','An inverse theorem for the Gowers U^{s+1}[N]-norm',2010,'B. Green, T. Tao and T. Ziegler')
zieg=a('1404.0775','Linear equations in primes and dynamics of nilmanifolds',2014,'T. Ziegler')
ban=a('1002.2259','Constructive Algorithms for Discrepancy Minimization',2010,'N. Bansal')
kom=a('1605.02882','An Algorithm for Komlós Conjecture Matching Banaszczyk\'s bound',2016,'N. Bansal, D. Dadush and S. Garg')
sm=a('2204.11427','Smoothed Analysis of the Komlós Conjecture',2022,'N. Bansal et al.')
far=a('1602.00999','Geometrization of the local Langlands correspondence: an overview',2016,'L. Fargues')
dia=a('1709.07343','Etale cohomology of diamonds',2017,'P. Scholze')
fs=a('2102.13459','Geometrization of the local Langlands correspondence',2021,'L. Fargues and P. Scholze')
k3=a('1004.0956','Notes on the K3 Surface and the Mathieu group M_24',2010,'T. Eguchi, H. Ooguri and Y. Tachikawa')
umb=a('1204.2779','Umbral Moonshine',2012,'M. C. N. Cheng, J. F. R. Duncan and J. A. Harvey')
proof=a('1503.01472','Proof of the Umbral Moonshine Conjecture',2015,'J. F. R. Duncan, M. J. Griffin and K. Ono')
onan=a('1702.03516',"O'Nan moonshine and arithmetic",2017,'J. F. R. Duncan, M. H. Mertens and K. Ono')

spec={
'P47': {'aliases':['virtual Haken conjecture','virtually special cube complexes','quasiconvex hierarchy','virtual fibering'], 'milestones':[
 ms('precursor',wise,'Wise sets out the quasiconvex-hierarchy structure','The 2011 manuscript develops cubical and special-group machinery used in the later proof.',[],kind='primary_text',note='The 2011 author listing is evidence of circulation, not a bibliographic publication record.'),
 ms('first_statement',agol,'Agol posts the virtual Haken proof','The preprint proves cubulated hyperbolic groups virtually special and states the 3-manifold consequence.',['Ian Agol'],note='The same proof states and applies the criterion.'),
 ms('first_application',agol,'Virtually special criterion settles virtual Haken','Agol applies the cubical criterion to closed hyperbolic 3-manifold groups.',['Ian Agol'],note='The same paper serves both the statement and its target application.'),
 ms('key_development',agolpub,'Virtual Haken proof appears in Documenta Mathematica','The journal record gives the later publication year.', ['Ian Agol'])],
 'people':[person('Ian Agol','developer','https://en.wikipedia.org/wiki/Ian_Agol',agol,'Proves virtual Haken using cubulated groups')],
 'notes':'The 2011 Wise manuscript is a precursor and has no checked bibliographic record for that date; the 2021 book record must not be backdated. No event-specific naming institution earlier than the proof was established.'},
'Q28': {'aliases':['relative Langlands duality','periods and L-functions','Hamiltonian dual spaces','electric-magnetic duality'], 'milestones':[
 ms('precursor',gw,'Gauge-theory boundary S-duality','The 2008 physics paper develops the boundary-condition duality used as analogy.',[],phase='gauge-theory analogy'),
 ms('precursor',sak,'Spherical-variety period framework','The 2012 work develops period and dual-group questions preceding the three-author proposal.',[],phase='relative Langlands'),
 ms('first_statement',bzsv23,'Relative Langlands proposal circulates publicly','An author-hosted first version gives the Hamiltonian-space duality and electric–magnetic analogy.',['David Ben-Zvi','Yiannis Sakellaridis','Akshay Venkatesh'],kind='primary_text',phase='relative Langlands',note='Publicly linked by July 2023, but the surviving PDF has no independent bibliographic record for its 2023 circulation.'),
 ms('key_development',bzsv24,'Proposal receives arXiv record','The named proposal has a dated public bibliographic record in September 2024.',['David Ben-Zvi','Yiannis Sakellaridis','Akshay Venkatesh'],phase='relative Langlands'),
 ms('institution',ober,'Oberwolfach Arbeitsgemeinschaft names the subject','A named workshop report treats relative Langlands duality systematically.',['David Ben-Zvi','Yiannis Sakellaridis','Akshay Venkatesh'],phase='relative Langlands')],
 'people':[person('Akshay Venkatesh','originator','https://www.math.ias.edu/~akshay/research.html',bzsv24,'Co-proposes relative Langlands duality')],
 'phases':['gauge-theory analogy','relative Langlands'],
 'notes':'The 2023 author-hosted draft precedes the 2024 arXiv record. It receives C-grade public-text evidence, not a fabricated 2023 bibliographic record. No first intentional application distinct from the proposal was established; searched the author site and arXiv abstract.'},
'Q65': {'aliases':['random hyperbolic surfaces','optimal spectral gap','Friedman-Ramanujan functions','tangle-free surfaces'], 'milestones':[
 ms('first_statement',fr1,'Friedman–Ramanujan surface programme begins','The first article defines functions designed to control the random-surface spectral gap.',['Nalini Anantharaman','Laura Monk'],note='The 2023 paper proves selected types, not yet the optimal gap.'),
 ms('first_application',fr1,'First spectral-gap estimates for selected geodesic types','The first article proves the Friedman–Ramanujan property for selected local types as an initial spectral-gap application.',['Nalini Anantharaman','Laura Monk'],note='The same paper serves both the first-statement and first-application roles.'),
 ms('key_development',tangle,'Tangles removed by Möbius inversion','A separate paper adapts a step from Friedman’s random-graph proof to condition on tangle-free surfaces.',['Nalini Anantharaman','Laura Monk']),
 ms('key_development',fr2,'Optimal random-surface spectral gap proved','The second article combines the estimates to show the first eigenvalue approaches at least one quarter in probability.',['Nalini Anantharaman','Laura Monk'])],
 'people':[person('Laura Monk','developer','https://en.wikipedia.org/wiki/Laura_Monk',fr2,'Co-proves the asymptotically optimal gap')],
 'notes':'The 2023 first part initiates and applies the method in selected cases, while the 2025 second part proves the stated target theorem. No separately named institution or course was identified in the arXiv records.'},
'B40': {'aliases':['quasiperiodic Schrödinger operators','Ten Martini problem','Schrödinger cocycles','global theory of one-frequency operators'], 'milestones':[
 ms('precursor',ten,'Ten Martini problem solved','An earlier dynamical/spectral result concerns the almost Mathieu operator, not the later global theory.',[]),
 ms('first_statement',avila,'Global one-frequency theory posted','Avila defines a stratified analytic framework for Lyapunov exponents and critical energies.',['Artur Avila'],note='The same work gives applications to spectral measures.'),
 ms('first_application',avila,'Cocycle dynamics applied to critical spectral energies','The paper uses complexified cocycle dynamics to show the critical set is typically thin.',['Artur Avila'],note='The same 2009 paper serves both statement and application of the global framework.'),
 ms('consolidation',avilapub,'Global theory published in Acta Mathematica','The journal article gives a later durable publication anchor.',['Artur Avila'])],
 'people':[person('Artur Avila','originator','https://en.wikipedia.org/wiki/Artur_Avila',avila,'Develops global one-frequency spectral theory')],
 'notes':'The Ten Martini result predates and is narrower than Avila’s global theory. The 2015 journal date is not its first public date.'},
'P70': {'aliases':['approximate groups','pseudofinite groups','model-theoretic approximate subgroups','Lie model theorem'], 'milestones':[
 ms('first_statement',hr,'Stable model theory meets approximate subgroups','Hrushovski’s public preprint develops a model-theoretic stabilizer method for approximate subgroups.',['Ehud Hrushovski'],note='The same paper states and applies the bridge.'),
 ms('first_application',hr,'Model-theoretic method applied to finite-set growth','The paper treats approximate subsets of linear groups and draws nilpotence consequences.',['Ehud Hrushovski'],note='The same paper truly plays both roles.'),
 ms('key_development',bgt,'General structure theorem for approximate groups','Breuillard, Green and Tao use nonstandard analysis and a Lie model to classify approximate groups.',['Emmanuel Breuillard','Ben Green','Terence Tao'])],
 'people':[person('Ehud Hrushovski','originator','https://en.wikipedia.org/wiki/Ehud_Hrushovski',hr,'Introduces model-theoretic tools to approximate groups')],
 'notes':'The inherited 2012 journal citation is later than the 2009 public preprint. The 2011 Breuillard–Green–Tao theorem is a distinct development, not the first model-theoretic transfer. Searched arXiv for a field-naming institution; none established.'},
'Q7': {'aliases':['amplituhedron','positive Grassmannian','positive geometry','on-shell diagrams'], 'milestones':[
 ms('precursor',pos,'Positive Grassmannian encodes amplitudes','The 2012 work directly maps scattering-amplitude operations to cells of the positive Grassmannian.',[],phase='positive Grassmannian'),
 ms('first_statement',amp,'Amplituhedron proposed','Arkani-Hamed and Trnka present the new geometric object for planar N=4 scattering amplitudes.',['Nima Arkani-Hamed','Jaroslav Trnka'],phase='amplituhedron',note='The same note makes the volume interpretation.'),
 ms('first_application',amp,'Scattering amplitudes identified with geometric volumes','The paper interprets planar amplitudes as amplituhedron volumes.',['Nima Arkani-Hamed','Jaroslav Trnka'],phase='amplituhedron',note='The proposal and target application are both in the same note.'),
 ms('naming',amp,'Amplituhedron appears in the paper title','The title supplies a reproducible term-use anchor.',['Nima Arkani-Hamed','Jaroslav Trnka'],phase='amplituhedron',note='The founding paper both proposes and names the object.')],
 'people':[person('Jaroslav Trnka','originator','https://en.wikipedia.org/wiki/Jaroslav_Trnka_(physicist)',amp,'Co-proposes the amplituhedron')],
 'phases':['positive Grassmannian','amplituhedron'],
 'notes':'The 2012 positive-Grassmannian paper is a precursor to the named 2013 amplituhedron, not a 2012 amplituhedron claim.'},
'QC8': {'aliases':['Gowers inverse theorem','nilsequences','Möbius-nilsequence orthogonality','linear equations in primes'], 'milestones':[
 ms('precursor',prime,'Prime-pattern strategy is stated conditionally','The 2006 paper makes the prime-counting goal conditional on the inverse theorem and Möbius–nilsequence conjecture.',[],phase='prime-pattern programme'),
 ms('precursor',mob,'Möbius orthogonality to nilsequences proved','One of the two needed inputs is established independently in 2008.',[],phase='nilsequences'),
 ms('first_statement',invann,'General Gowers inverse theorem announced','The June 2010 public announcement states nilsequence control for all higher Gowers norms.',['Ben Green','Terence Tao','Tamar Ziegler'],phase='inverse theorem'),
 ms('first_application',invann,'Inverse theorem yields prime-pattern asymptotics','The announcement identifies unconditional consequences for finite-complexity linear equations in primes.',['Ben Green','Terence Tao','Tamar Ziegler'],phase='prime-pattern programme',note='The same announcement serves both roles: it states the theorem and applies earlier transference results to primes.'),
 ms('key_development',inv,'Full inverse-theorem proof posted','The September 2010 preprint supplies the detailed proof following the June announcement.',['Ben Green','Terence Tao','Tamar Ziegler'],phase='inverse theorem'),
 ms('consolidation',zieg,'Nilmanifold-dynamics survey','A survey explains the number-theoretic and ergodic-theoretic chain.',['Tamar Ziegler'],phase='prime-pattern programme')],
 'people':[person('Tamar Ziegler','developer','https://en.wikipedia.org/wiki/Tamar_Ziegler',inv,'Co-proves higher-order Gowers inverse theorem')],
 'phases':['prime-pattern programme','nilsequences','inverse theorem'],
 'notes':'The June 2010 announcement predates the September 2010 full proof. The 2006 prime theorem is conditional at higher complexity; the inverse and Möbius results remove these conditions.'},
'Q3': {'aliases':['algorithmic discrepancy theory','constructive discrepancy','Komlós conjecture','vector balancing'], 'milestones':[
 ms('first_statement',ban,'Constructive discrepancy breakthrough posted','Bansal gives polynomial-time algorithms matching key existential discrepancy bounds.',['Nikhil Bansal'],note='The same paper applies its method to classical set discrepancy.'),
 ms('first_application',ban,'Algorithm attains Spencer-type discrepancy bounds','A semidefinite-programming-based constructive method targets discrepancy minimization.',['Nikhil Bansal'],note='The founding paper serves both first-statement and first-application roles.'),
 ms('key_development',kom,'Algorithm reaches Banaszczyk Komlós bound','The later algorithm matches the best then-known nonconstructive bound, without proving the constant-bound conjecture.',['Nikhil Bansal']),
 ms('key_development',sm,'Smoothed Komlós case proved','The conjecture is proved for a perturbed-input regime, a conditional model rather than the full conjecture.',['Nikhil Bansal'])],
 'people':[person('Nikhil Bansal','originator','https://en.wikipedia.org/wiki/Nikhil_Bansal',ban,'Develops constructive discrepancy algorithms')],
 'notes':'The 2016 result matches Banaszczyk’s bound and the 2022 result proves a smoothed model; neither settles the full Komlós conjecture. Searched the cited papers for an event-specific named institution and found none.'},
'Q42': {'aliases':['Fargues–Scholze correspondence','geometric local Langlands','Fargues–Fontaine curve','diamonds'], 'milestones':[
 ms('precursor',far,'Fargues states local geometrization conjecture','The 2016 overview publicly formulates the programme before the joint construction.',[]),
 ms('precursor',dia,'Diamonds supply geometric foundations','Scholze develops the étale cohomology of diamonds used by the later framework.',[]),
 ms('first_statement',fs,'Fargues–Scholze geometrization posted','The joint preprint builds sheaf categories on the Fargues–Fontaine curve and geometric Satake.',['Laurent Fargues','Peter Scholze'],note='The same preprint states and applies the framework.'),
 ms('first_application',fs,'Local Langlands parameters constructed','The theory attaches L-parameters to irreducible smooth representations of p-adic groups.',['Laurent Fargues','Peter Scholze'],note='The same paper both sets out the framework and proves this target application.')],
 'people':[person('Peter Scholze','developer','https://en.wikipedia.org/wiki/Peter_Scholze',fs,'Co-develops the geometric framework and constructs L-parameters')],
 'notes':'Fargues’s 2016 conjecture and Scholze’s 2017 diamonds are precursors to the joint 2021 paper. This is not a claim of a complete bijective local Langlands correspondence. No earlier named institutional anchor was verified.'},
'Q58': {'aliases':['Mathieu moonshine','umbral moonshine','O\'Nan moonshine','pariah moonshine','mock modular forms'], 'milestones':[
 ms('precursor',k3,'K3–Mathieu observation','The elliptic genus of K3 is related to Mathieu group representation dimensions.',[],phase='Mathieu moonshine'),
 ms('first_statement',umb,'Umbral moonshine conjecture formulated','The 2012 paper relates mock modular forms to a family of finite groups.',['Miranda Cheng','John F. R. Duncan','Jeffrey Harvey'],phase='umbral moonshine'),
 ms('naming',umb,'Umbral moonshine named in title','The paper title gives a dated term-use anchor.',['Miranda Cheng','John F. R. Duncan','Jeffrey Harvey'],phase='umbral moonshine',note='The same paper both formulates and names the conjecture.'),
 ms('first_application',umb,'Mock modular forms linked to umbral groups','The founding paper deliberately uses the conjectured group correspondence to organize mock modular forms.',['Miranda Cheng','John F. R. Duncan','Jeffrey Harvey'],phase='umbral moonshine',note='The same paper serves both proposal and first-application roles.'),
 ms('key_development',proof,'Umbral moonshine conjecture proved','The proof constructs and identifies the predicted moonshine modules.',['John F. R. Duncan','Michael J. Griffin','Ken Ono'],phase='umbral moonshine'),
 ms('key_development',onan,"O'Nan moonshine links a pariah group and arithmetic",'A separate 2017 paper constructs a graded O\'Nan module whose series are weight-3/2 modular forms.',['John F. R. Duncan','Michael H. Mertens','Ken Ono'],phase="O'Nan moonshine")],
 'people':[person('John F. R. Duncan','developer','https://en.wikipedia.org/wiki/John_F._R._Duncan',proof,'Co-proves umbral moonshine and develops the later O\'Nan branch')],
 'phases':['Mathieu moonshine','umbral moonshine',"O'Nan moonshine"],
 'notes':'The 2010 K3 observation, 2012 umbral conjecture, 2015 proof, and 2017 O\'Nan branch are separate milestones. The 2012 paper gives the first application of its framework; the 2015 proof is a later decisive development.'}
}

spec['Q28']['milestones'][2]['evidence'].append({'claim': 'A dated July 2023 account links the already circulating first draft', 'source': 'Columbia mathematics blog', 'url': 'https://www.math.columbia.edu/~woit/wordpress/?p=13578', 'kind': 'history_page'})

def main():
    rows=[]
    for event in json.loads((BASE/'batch49.json').read_text()):
        item=spec[event['eventId']]
        rows.append({'pid':event['pid'],'eventId':event['eventId'],'canonicalName':event['name'],
                     'aliases':item['aliases'],'phases':item.get('phases',[]),
                     'milestones':sorted(item['milestones'],key=lambda e:e['year']),
                     'people':item['people'],'notes':item['notes']})
    (BASE/'milestones49.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    print(f"Wrote {len(rows)} events and {sum(len(e['milestones']) for e in rows)} milestones")
if __name__=='__main__':main()
