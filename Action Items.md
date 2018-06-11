## Misc Items

(none)


## Deliverables

### GitHub Repo
 * Create a GitHub repository for the group. Each member should be added as a contributor.  (DONE)
 * Retrieve the dataset and upload it into a directory named assets.  (DONE, but may want a cleaner dir structure)
 * Generate a .py or .ipynb file that imports the available data.  (JW)

### Project Planning
 * Define your deliverable - what is the end result?  (DONE?)
 * Break that deliverable up into its components, and then go further down the rabbit hole until you have actionable items. Document these using a project managment tool to track things getting done. The tool you use is up to you; it could be Trello, a spreadsheet, GitHub issues, etc. (JT - I think this document is the planning document)
 * Begin deciding priorities for each task. These are subject to change, but it's good to get an initial consensus. Order these priorities however you would like. (JT)
 * You planning documentation (or a link to it) should be included in your GitHub repo.  (DONE - It's this document until further notice)


### EDA
 * Describe the data. What does it represent? What types are present? What does each data points' distribution look like? Discuss these questions, and your own, with your partners. Document your conclusions. (JW; SL; JT)
 * What kind of cleaning is needed? Document any potential issues that will need to be resolved. (JW; SL; JT)

### Modeling
 * The goal is of course to build a model and make predictions that the city of Chicago can use when it decides where to spray pesticides! Your team should have a clean Jupyter Notebook that shows your EDA process, your modeling and predictions.
   * Individual notebooks (SL; JT; JW)
   * Ensemble notebook (JT)
 * Conduct a cost-benefit analysis. This should include annual cost projections for various levels of pesticide coverage (cost) and the effect of these various levels of pesticide coverage (benefit). (Hint: How would we quantify the benefit of pesticide spraying? To get "maximum benefit," what does that look like and how much does that cost? What if we cover less and therefore get a lower level of benefit?)
   * Get cost of disease per patient (JT -- DONE.  It's approx 25k$ per hospitalization)
   * Get municipal cost of spraying (SL)
   * Just see if neighborhoods that got sprayed had lower (WNV * num_mosquitoes) afterward (JT)
 * Your final submission CSV should be in your GitHub repo. (JT)
 * Finalize code for cleaned predictor matrix by Tuesday morning. I think this will take the form of a *.py file
 which contains functions.  Each function adds a column to the dataframe, or joins dataframes.  At the end of the file, all the functions run in sequence.  Then the output is sent to a csv, and everybody's notebooks can just read in that csv, with however many columns it ends up being.  Whoever compiles all this will have to resolve duplicate column names if they arise. (JW?)
 * Everybody test their models by Wed. morning, push final notebooks to repo (SL, JT, JW)
 * Run ensemble code by Thursday morning, push notebook to repo. (JT)

### Presentation
 * Audience: You are presenting to members of the CDC. Some members of the audience will be biostatisticians and epidemiologists who will understand your models and metrics and will want more information. Others will be decision-makers, focusing almost exclusively on your cost-benefit analysis. Your job is to convince both groups of the best course of action in the same meeting and be able to answer questions that either group may ask.
 * The length of your presentation should be about 20 minutes (a rough guideline: 2 minute intro, 10 minutes on model, 5 minutes on cost-benefit analysis, 3 minute recommendations/conclusion). Touch base with your local instructor... er, manager... for specific logistic requirements!
   * Intro + conclusions (JW)
   * Modeling (JT)
   * Cost-benefit (SL)
 * Outline for presentation segments due to editor Thu afternoon
 * Editor finalizes presentation Thu. night. (???)
