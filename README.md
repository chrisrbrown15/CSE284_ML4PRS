# CSE284_ML4PRS

## Predicting Colorectal Cancer Risk Using a Polygenic Risk Score and Machine Learning Methods

data source: https://odap-ico.github.io/PRS_tutorial/#whats-a-polygenic-risk-score

### Dataset & Preprocessing
This study employs a case–control design to evaluate the performance of a PRS for CRC. Publicly available data from the GitHub repository (https://github.com/odap-ico/PRS_tutorial) will be used. The dataset includes individual-level genotype data in VCF format, effect size estimates for 205 single-nucleotide polymorphisms (SNPs) associated with CRC, and phenotype labels for 486 CRC cases and 3,783 controls. Data preprocessing will include the removal of duplicate SNPs, filtering variants with low minor allele frequency, and the use of LD-clumping to choose a set **𝑆**of independent SNPs with strong signals. Quality control and data preparation will be performed using PLINK and R, while genotype extraction from VCF files will be conducted using the PyVCF Python package.

### Methods

The baseline PRS will be defined as 𝑃𝑅𝑆𝑖 = (𝛽𝑇 𝑋𝑖) for effect sizes 𝛽 from GWAS and genotypes 𝑋𝑖 for individual 𝑖. The PRS will be transformed into a probability score through logistic regression by learning values of 𝛾0 and 𝛾1 for 𝐿𝑜𝑔𝑖𝑡(𝑃𝑖) = 𝛾0 + 𝛾1( 𝛽𝑇 𝑋𝑖). To compare against the baseline PRS model, we will utilize logistic regression, random forest, and neural network models to predict CRC status using weighted genotypes as features. Genotypes will be encoded as minor allele dosages {0,1,2}, representing the number of minor alleles carried by an individual at each SNP. Each genotype will then be multiplied by its corresponding GWAS effect size (β coefficient), resulting in weighted genotype features that incorporate both allele count and estimated effect magnitude. Class-weighting will be used during training. Regularization will be utilized to prevent overfitting. Data will be split into train, validation, and test sets. Due to class imbalance, model performance will be evaluated using F1-score and precision-recall AUC.
