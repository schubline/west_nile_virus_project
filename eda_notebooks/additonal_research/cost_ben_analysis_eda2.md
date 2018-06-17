# Cost Benefit Analysis EDA

## Project Guidelines
Conduct a cost-benefit analysis. This should include annual cost projections for various levels of pesticide coverage (cost) and the effect of these various levels of pesticide coverage (benefit). (Hint: How would we quantify the benefit of pesticide spraying? To get "maximum benefit," what does that look like and how much does that cost? What if we cover less and therefore get a lower level of benefit?)


Calculate centroid, standard dev of radius
## General Stats
- Num Cases
- Societal costs of WNV in general, attempt to specify for Chicago


## Municipality methods of Prevention

### WNV Vaccination
**Source:** [Cost Effectiveness of WNV Vaccination](https://wwwnc.cdc.gov/eid/article/12/3/05-0782_article#tnF1)

**Key Takeaways**
1)
2)
3)

Figures:
- [Decision tree for vaccination program. WNV, West Nile virus](https://wwwnc.cdc.gov/eid/article/12/3/05-0782-f1)


### Truck Sprays
- Spray Costs
  - Zenivex E40: Targets adult mosquitos. Spray at dusk.  
  - back of napkin math/ code to get the spray area, do costs, for x amount of traps
- Uber Kepler GL Visualization
- join on train in order to get that amount of mosquitoes present with spray

### Epidemiology & Surveillance
**Sources**
- [Current Trends in WNV Vaccine Development](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4279923/)
-


### Awareness Campaigns
- Citizen Methods of Prevention

##

## Additional links

http://chicago.cbslocal.com/2017/08/30/spray-mosquitoes-far-south-side-west-nile-prevention/

https://www.nbcchicago.com/news/local/City-to-Spray-Mosquito-Killing-Insecticide-Wednesday-Night-322342752.html

## if not looking at pray data; case yould be
-  predict presense of WNV, maybe bring in some outside estimates for the effects of spraying, the cost of spraying, the cost of hospitalizations.
- talk to city statiticians,
- The recoomendation that we're making is to help you predict where WNV will show up and help you take the best
- used features as best predictor of occurance of WNV.
- Caveat about spray analysis being simplicfication of reality.

## Spray Processing
- HDBSCAN
- Condense to
  - date, lat, lon, stf
- make new binary columns for train/test
  -  sprayed 0/1
- time since spray
  Dummy columns
    - 0-2 weeks ago
    - 2-4 weeks ago
    - Everything else

- For each cluster on each day

- Radiums = 2 * (lat^2 + lon^2)^-1/2, x_bar of cluster 'centroid'
- T-test to see if sprayed neighborhhods, run the average; if neighborhoods were randomly sampled
- top of slide (assumptions)
- join both spray and train
- then make explainable logistic  regression
