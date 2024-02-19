
Search
Write

Rich Lin
Get unlimited access to the best of Medium for less than $1/week.
Become a member


Raising the bar by lowering the bound
Why tackling overestimation is essential for product development
Nils Skotara
Booking.com Data Science
Nils Skotara

·
Follow

Published in
Booking.com Data Science

·
16 min read
·
Nov 1, 2023
84


1





Kelly Pisane
 
Nils Skotara

TL;DR:
Using point estimates to measure the impact of interventions can be highly misleading. In order for the sample mean to be an unbiased estimator of the population mean, there must be a guarantee that experimenters will under no circumstances deviate from the execution plan of the experiment and won’t impose any selection on which impact estimates will be kept. However, because experiments need to be stopped early when results are detrimental and results of stopped interventions won’t have any future business impact, we bias our estimator. As a result, estimates obtained are usually overly optimistic, and favor under powered experiments. Using the lower (conservative) bound of the confidence interval is a viable practical alternative that takes uncertainty into account and provides a counterbalance against overestimation that is larger for low quality experiments and settings with many false positives.

Overview
Online companies such as Booking.com leverage experimentation to measure the impact of product changes on the customer experience. This involves comparing the current version of the website with a new version that contains the product change and measuring which one leads to a better outcome, for example a higher conversion rate. However, as an additional objective of experimentation, it is also desirable to measure the magnitude of the impact. Typically, it is assumed that the point estimate (observed difference between the current and new version) of the test is an unbiased estimator of the true impact. Unbiased means that there is no systematic over or underestimation. However, and perhaps surprisingly, this isn’t the case in practical scenarios. In practice, the decisions that the experimenters make are influenced by the data; for example, stopping an experiment early because the results look detrimental. As soon as we make any such decisions, the point estimates become biased and can severely overestimate the true impact. Moreover, underpowered experiments and experiments that don’t follow the experimentation protocol while showing significant effects gain an unfair advantage since they lead to more severe overestimation than their well conducted counterparts. A fair comparison between different experiments is impossible when looking at the point estimate because it does not take uncertainty into account. In this blogpost, I will show how business decisions introduce bias that causes impact estimates using the point estimate to be misleading. Further, I will discuss the repercussions of relying on misleading results and show a practical solution. The ideal way to address these issues would be to use an alternate data set that has not been included in the decision making to estimate impact. Here I will discuss a practical alternative when we are not able to obtain such a dataset: The use of the lower bound of the confidence interval.

Unbiased estimators?
In online experimentation, the observed difference between the new product and the old version is an unbiased estimator of the true unknown effect of the product change. For example, if the conversion rate of the old website was measured at 20% and the product change consisting of a design overhaul led to a conversion rate of 23%, the unbiased estimate for the true absolute impact of the design change is 23% — 20% = 3%. To be an unbiased estimator, the procedure of calculating a value from a sample should neither systematically over nor underestimate the population value. In case of online experimentation, this means that if we could run the same experiment many times the mean of the estimates of the difference between the control group and the treatment group obtained would be equal to the population mean, or the true impact of the product change. This sounds like a great property and the business seems to be well advised to use this estimator for its prioritization and long term planning, but in practice this is not the case. In this article I will argue that using the point estimate can even be dangerous and explain why its unbiasedness breaks down. But first let’s have a closer look into how the term unbiased is defined.

What is unbiasedness
When customers enter the website, we randomly allocate them either to the current version (the control group) or the new version of the website (the treatment group). Without any loss of generality, we will assume that we will have n customers in both groups. The values that a metric can take for every customer in the control group can be written as Xᵢ , where all values are drawn from independent and identical distributions with a population mean μₓ and variance σ²ₓ (similar conclusions can be drawn with less strict assumptions). In the conversion example this means xᵢ ∈ {0, 1}, where 1 represents a conversion and 0 represents no conversion. Thus, the mean of all values in the control group which consists of n customers is n⁻¹∑ᵢXᵢ which in our particular experiment will have an observed value of n⁻¹∑ᵢxᵢ which, because xᵢ is binary, equals the number of visitors who converted divided by the total number of visitors. Similarly, we can do the same for the treatment group, that we call Z instead of X. For simplicity, it also consists of n customers. Thus, for the average treatment effect, we will have the difference of these two sums:


To see why this calculation leads to an unbiased estimator for the population mean, we use the linearity of the expectation:


This means that we can write:


In other words, the expected difference of the mean in the control group and the mean in the treatment group is equivalent to the expectation of the difference of the population means. Because we randomly assign all visitors to either control or treatment, this difference can be interpreted as the causal effect of our product change.

The role of variance in estimations
You might have noticed that the notion of unbiasedness does not depend on the sample size n in any way, in other words, if we take samples of 1 visitor (we plug in n = 1), we already have an unbiased estimator because:


However, we would not base a decision on a sample with just one visitor. Samples will drastically differ from each other, with estimated conversion rates of either 1 or 0 for every sample. Thus, the variance of the estimator (between samples) is of crucial importance. The variance can be written as follows:


Using (writing ∑ᵢXᵢ=s for simplicity):


Which in turn uses:


It shows that the variance of the mean decreases by a factor of n where n is the sample size. Thus, the standard error decreases by a factor of square root of n, which implies that if we want to reduce the standard error of the estimator by a factor of 10 we need to increase the sample size by a factor of 100. Figure 1 shows how this looks like for n = 1000, n = 10000, and n = 50000.


Figure 1. The distribution of average treatment effect (ATE) for different sample sizes. Each density is based on 10000 experiments with a sample size of n in base and in variant. We can see that the variance decreases with increasing numbers of samples..
The importance of the variance can’t be stressed enough for two main reasons:

An estimator that is unbiased can still lead to a value very far from the population mean in a particular sample when it has large variance
The higher the standard error is, the lower the power of the experiment is and the more likely we are to miss an impactful product change
This means that, even by using an unbiased estimator, an individual measurement may be far from the population mean, and in a business context we generally will not run the same experiment many times. The fact that the estimator obtained from a randomized sample is theoretically unbiased, does not provide us much direct benefit in determining the impact of our product changes. We should, rather, judge the quality of an estimator in light of its associated uncertainty, namely the variance and all measures derived from it such as the standard error and the confidence interval we are interested in.

Decisions introduce bias
So far, we have seen that unbiasedness doesn’t provide much benefit for a single sample, particularly if the sample isn’t very large. However, the problem gets compounded when we consider how the results of experiments are used and reported. Usually, a successful product change will be shipped and included in the business’s financial reporting, prioritization and evaluation of the team’s success. Unsuccessful product changes will simply be discarded. This simple and common selection of those results that are promising and there to stay, and those that are not, completely destroys the notion of unbiasedness. When the results are used to determine whether an estimate will be used, it introduces m-error (m stands for magnitude). It refers to the fact that after such a selection, our estimates are systematically too high and severely overestimate the true impact of the product change, the average overestimation increases with decreasing statistical power. The next section will explain the m-error in a bit more detail.

The m-error
The following explanations assume that the alternative hypothesis is true. Would the Null hypothesis be true, or the effect be in the reverse direction, the overestimation would be even worse. The significance threshold of a statistical test divides the distribution of the effect under the Null hypothesis as well as the distribution of the effect under the alternative hypothesis into two parts. By selecting only significant results, the distribution of the means, e.g. average treatment effect (the sampling distribution) gets truncated and results that don’t pass the significance threshold do not enter the calculations. Thus, the mean of this truncated distribution is systematically too high. This overestimation is worse for experiments with low power and large uncertainties.


Figure 2. The setup of a significance test for an experiment. The Null hypothesis (H0) states that there is no effect, meaning that the estimate of the average treatment effect comes from a distribution that is centered around 0. The alternative hypothesis (H1) states that the effect is positive. The significance threshold (vertical line) depends only on the distribution under H0. The proportion of the area of H1 that lies to the right of the threshold is the power of the test. When the effects that get reported are selected based on the significance of the result, The red distribution gets truncated.

Figure 3. When selecting which effects get reported based on the significance of the results, the distribution gets truncated more for smaller power and less for higher power of the experiment. (The numbers aren’t exact since the plots were generated using simulation code rather than the integral calculation.)
Thus, aggregating the impact over successful product changes means that the estimates are off by huge amounts and the business is overly optimistic on all levels of reporting. Even when all of the effects are real effects (no false positives, all coming from the red distribution) there will be m-error due to the truncation of the distributions as shown in figure 3 above. The m-error shown here does not take into account the part of the green distribution that also falls to the right of the decision threshold. Those data aren’t technically subject to the m-error but rather to the alpha error of incorrectly rejecting the null hypothesis. In a practical scenario however, they also contribute to the overestimation of the results. This is crucial since, in practice, a large number of experiments will show conclusive results even if there is no effect. They are drawn from the green distribution. When our power is low, the contribution of the red distribution to the right of the cutoff decreases, but the contribution of the green distribution (no effect) stays the same. This means that the actual overestimation that we would observe in practice is even larger than the theoretical m-error, which refers exclusively to the red distribution. The m-error is infinite in that sense when looking at the green distribution alone.

Deeper explanation
The deeper reason for this overestimation bias is that we are using the same dataset for two different purposes: making a decision whether or not the new product should be shipped and attempting to estimate how large the impact of the new product is. Anytime we are using a single dataset for more than one purpose, we are getting ourselves into serious trouble. It has been well known within statistics that none of the estimators and statistical inferences are correct if a dataset is used for exploratory analyses and statistical inference at the same time. Anytime the model used depends in any way on the data that the model is supposed to represent, the model itself is the result of a random process which is too complicated and complex to capture formally. Thus, in order to have correct results, we absolutely and necessarily need to either preregister everything we do OR use different datasets for different purposes. While the practice of separating datasets for modelling and evaluation has become widely accepted in the AI and Machine Learning community it is not as commonly used in statistical analysis and other areas of Data Science. If we pick a model that minimizes the in-sample loss (the sample mean is already one such model!), we do empirical risk minimization. This however leads to overoptimism and overfitting, due to sampling variability introducing noise into our estimation of risk with the in-sample loss, which depends on the data and the true parameter .


In-Sample Loss = Risk + Sampling Noise
The problem is that the model that minimizes the in-sample loss could either generalize well by having a small risk, which depends on the true distribution and the true parameter, or may not generalize well as it has moderate risk but be based on a sample with a large negative sampling noise component. With a single sample, there is no way to determine which scenario we are in. By using data to select the model, at the very least we increase the probability that sampling noise dominates the in-sample loss. This is why picking the model that best fits the data or picking a model that has preferred properties based on the data is overly optimistic with regards to their generalization error. In other words, all statistical theory assumes that the model was fixed in advance, if it wasn’t then all theory becomes invalid. The m-error is but a special case of this phenomenon: The model in case of online experimentation is the arithmetic mean of the empirical distribution. Naturally, the ones with sampling noise leading to a positive significant test decision are more likely to be kept. Those ones in turn, are more likely included in aggregations than those models with ‘unfavorable’ sampling noise. Straightforward remedies to this situation are using different datasets for different purposes, for example with cross-validation. It works because E[L(X,Θ)] stays the same over repeated folds of the data whereas ηₙ(Θ) will behave like noise.

The optimal solution: Retesting
The only way to select successful variants AND report their individual impacts unbiasedly is to have separate datasets for evaluation and impact estimation. This can be achieved either by retesting every successful experiment or having a per-experiment holdout dataset. With either of these methods, we get an unbiased estimator of the impact. In a business context however, either of these options can increase the time to reach a decision and take additional time away from product development cycle. Even if these short term costs are massively overshadowed by the improved quality of all long term decisions, businesses can be hesitant to adopt a strict retesting policy or chose to only retest really crucial products. Before I describe a pragmatic solution to this dilemma, I will briefly discuss why often stated potential alternatives are not well suited to successfully mitigate this issue.

Alternatives
Bayesian Methods
Bayesian ways of estimating the impact of experiments require a lot of assumptions and don’t fundamentally address the m-error. A main idea is to use the treatment effect estimates from a large number of experiments to adjust the individual estimates of each experiment. Often there is the assumption that impact is normally distributed. Which is not justified by large samples alone; it implies similar distributions of possible effect sizes across different areas of the business as well as a certain heterogeneity of the impact of product changes. Even with these assumptions, the shape of the posterior distribution depends crucially on the size of the tails of the prior distribution of the impact of product changes. Incorrectly assuming that the prior has thin Gaussian tails resulted in large biases in the posterior impact distribution (Azevedo et al. 2019). Moreover, there is evidence that a small number of bold product changes account for a large portion of the overall impact, even in mature internet companies such as Bing. Most fundamentally, Bayesian protocols usually lead to a simple shift of the significance threshold e.g. it is considered optimal to implement product changes with a larger t-statistic than the usual significance threshold. Thereby, these procedures do not fundamentally address the m-error problem in a systematic way. A larger threshold makes sure that the declared winners usually have smaller standard errors and that in turn makes it likely that they were sufficiently powered. On the one hand this makes sure that among those the m-error should be kept very small. On the other hand, this sets many previous wins to 0, essentially underestimating the overall impact of many efficient product changes. In summary, Bayesian methods usually shift the threshold, which leads to successful experiments having less overestimation at the expense of missing many product changes. The overall impact on the m-error remains unaddressed.

Meta Analyses
Meta analyses usually reweight different estimates to reach an overall estimate. This method is essentially only suitable if all the individual estimates aim to measure the same phenomenon. Moreover, any pre-selection will suffer from m-errors. Usually in a business context, we aim to aggregate the impact of many different types of product changes and can’t get around the selection problem. Insignificant product changes weren’t shipped and thus are not impacting the final product anymore, including them in any aggregated impact analyses simply doesn’t make sense.

Business solution
All considerations so far only get worse when considering aggregations of impact over large groups of experiments. In summary, measuring the impact with the observed mean (the point estimate) strongly overestimates impact and underestimates harm, while ignoring uncertainty and favoring low-quality / underpowered experiments. Faced with this necessary selection mechanism based on the decision, there is no way of having an unbiased estimator without an independent dataset, aka retesting experiments. What can we do instead? A reasonable estimator in this context should account for the uncertainty in the data and it should favor high quality experiments with large sample sizes, low uncertainties, and sufficiently high power over low sample sizes / low power. For this reason, an alternative, fairer way of measuring impact which supports strategic business considerations is to use the lower bound of the 95% one-sided confidence interval. On the one hand this will underestimate the impact when looking only at true effects, on the other hand it will:

Lead to an impact estimation that is much closer to the truth when estimated over all successful experiments which includes false positives.
Favor high quality experiments with good power over low quality experiments with low power.
Simulation Analysis
We simulated a total of 100,000 experiments in total out of which 70,000 were underpowered, 40,000 peeked 3 times at the results, and 15,000 had a true business impact. These were drawn independently and completely at random. We have used a one sided alpha of 0.05. These experiments had different violations of the proper experimental protocol. They were either properly powered (0 violation), underpowered (1 violation), or underpowered in combination with peeking issues (2 violations). Peeking was simulated by checking results 3 times after each incoming third of data instead of 1 time at the end of the experiment. This is probably optimistic compared to the peeking behavior in many online companies. Underpowered experiments were drawn from a distribution with an average power of 0.6 and a standard deviation of 0.04, thus 95% of all underpowered experiments had powers between 0.52 and 0.68. Properly powered experiments were drawn from a distribution with an average of 0.8 and a standard deviation of 0.04, thus 95% of all well powered experiments ended up having between powers of 0.72 and 0.88.


Figure 4. Overall results of the simulations. Bias in units of standard errors on the y-axis is plotted against the three categories of experimentation quality for the lower bound (dark blue), the (true, unbiased and unknown) real effect (yellow), and the point estimate (light blue). The left side shows the average per experiment and the right side depicts the sum over all experiments in this simulation setup.
Figure 4 shows the results of the simulations. When looking at experiments that displayed a significantly positive result, the point estimate overestimated the impact by 1 standard error in the case of no violations, 2 standard errors in case of low power, and 2.5 standard errors for experiments that peeked as well. In contrast, the lower bound underestimates by less than 1 standard error in most cases and does not systematically favor lower quality experiments with more protocol violations. This is particularly striking when looking at the sums, where the lower bound ensures comparability whereas the point estimate drastically inflates the impact of low quality experiments. In a business context, over the course of months, this leads to systematically misleading product decisions (by over 30.000 standard errors in this case) and an unfair disadvantage of product teams that adhere to a proper experimental protocol.


Figure 5. Results of the simulations broken down into false positives and true positives (real effects). Keep in mind that this distinction is possible in a simulation context only and in practice, it is unknowable which experiments belong to which of these groups. Bias in units of standard errors on the y-axis is plotted against the three categories of experimentation quality for the lower bound (dark blue), the (true, unbiased and unknown) real effect (yellow), and the point estimate (light blue). The left side shows the average per experiment and the right side depicts the sum over all experiments in this simulation setup.
Figure 5 further differentiates the impact that false positives and true positives (labeled as real effects) have on these results. We can see that the point estimate consistently favors low quality over high quality and dramatically overestimates the true impact by up to 3 standard errors per experiment. This amounts to a bias of more than 17000 standard errors over the course of 100,000 experiments. Interestingly, even among the true positives, the overestimation of the point estimate is further away from the truth for experiments with protocol violations. The point estimate looks best for the lowest quality experiments, while it should be the other way around. The lower bound instead, displays the lowest underestimation or negative bias for the best quality experiments and favors those over the experiments that violate the protocol. In summary, the lower bound sets the right incentives and misestimates less than the point estimate in a realistic business scenario.

Conclusion
Decision making based on experimental results introduces a bias to the point estimate for which no theoretically sound correction mechanism exists. This bias overestimates and favors low quality, underpowered interventions. Therefore, it is important to apply a mitigation strategy by using an impact estimation that has more desirable properties, namely taking the uncertainty into account and favoring high quality experiments. The statistically optimal solution to this problem would be to retest every single successful product change. In a business context, this is often not possible nor desired. Thus, a pragmatic approach that works surprisingly well is to use the lower bound of the 95% one-sided confidence interval for impact estimation and reporting instead.

Acknowledgements
Karol Podkanski

References
Eduardo Azevedo; Alex Deng; José L. Montiel Olea and E. Glen Weyl, (2019), Empirical Bayes Estimation of Treatment Effects with Many A/B Tests: An Overview, AEA Papers and Proceedings, 109, 43–47

Featured
84


1




Nils Skotara
Booking.com Data Science
Written by Nils Skotara
86 Followers
·
Writer for 
Booking.com Data Science

Data Scientist, passionate about the scientific method and its applications, particularly statistics and causal inference.

Follow

More from Nils Skotara and Booking.com Data Science
Sequential Testing at Booking.com
Nils Skotara
Nils Skotara

in

Booking.com Data Science

Sequential Testing at Booking.com
Reliable and fast product decisions
14 min read
·
Jun 12, 2023
279

3



How Booking.com increases the power of online experiments with CUPED
Simon Jackson
Simon Jackson

in

Booking.com Data Science

How Booking.com increases the power of online experiments with CUPED
Simon Jackson |Data Scientist at Booking.com
8 min read
·
Jan 22, 2018
1.6K

15



Don’t be tricked by the Hashing Trick
Lucas Bernardi
Lucas Bernardi

in

Booking.com Data Science

Don’t be tricked by the Hashing Trick
In Machine Learning, the Hashing Trick is a technique to encode categorical features. It’s been gaining popularity lately after being…
12 min read
·
Jan 10, 2018
1.5K

7



Encouraged to comply
Nils Skotara
Nils Skotara

in

Booking.com Data Science

Encouraged to comply
Improving bounds with Instrumental Variables
14 min read
·
Aug 4, 2022
25

1



See all from Nils Skotara
See all from Booking.com Data Science
Recommended from Medium
How good are your ML best practices?
George Chouliaras
George Chouliaras

in

Booking.com Data Science

How good are your ML best practices?
by  George Chouliaras, Kornel Kielczewski, Amit Beka, David Konopnicki and Lucas Bernardi
10 min read
·
Aug 23, 2023
63

1



Tackling UX challenges as a team
Evan Karageorgos
Evan Karageorgos

in

Booking.com — UX Writing

Tackling UX challenges as a team
A process for rapid group ideation
6 min read
·
Aug 31, 2023
62



Lists



Staff Picks
574 stories
·
730 saves



Stories to Help You Level-Up at Work
19 stories
·
463 saves



Self-Improvement 101
20 stories
·
1311 saves



Productivity 101
20 stories
·
1202 saves
Enhancing the Customer Experience with Machine Learning: Personalized Meal Recommendations using…
Sophie Kohoutek
Sophie Kohoutek

in

HelloTech

Enhancing the Customer Experience with Machine Learning: Personalized Meal Recommendations using…
by Vanya Kostova
5 min read
·
Dec 7, 2023
7



Beyond A/B test : Speeding up Airbnb Search Ranking Experimentation through Interleaving
Qing Zhang
Qing Zhang

in

The Airbnb Tech Blog

Beyond A/B test : Speeding up Airbnb Search Ranking Experimentation through Interleaving
Introduction of Airbnb interleaving experimentation framework, usage and approaches to address challenges in our unique business
10 min read
·
Oct 6, 2022
340

4



How to avoid KPI psychosis in your organization?
Ágoston Török
Ágoston Török

in

Promaton

How to avoid KPI psychosis in your organization?
A practical guide to a good measurement culture where numbers don’t replace common sense
5 min read
·
Aug 22, 2023
203

2



Get to know: Ronan Bradley, VP of Product Analytics and User Research for Facebook at Meta
Analytics at Meta
Analytics at Meta

Get to know: Ronan Bradley, VP of Product Analytics and User Research for Facebook at Meta
Q: Let’s start with the basics… What is your role at Meta?
8 min read
·
Jan 30
75

2



See more recommendations
Help

Status

About

Careers

Blog

Privacy

Terms

Text to speech

Teams