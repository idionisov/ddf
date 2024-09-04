from scipy.stats import beta

def clopper_pearson_interval(
    passed: int,
    total: int,
    confidence_level: float = 0.6826894921370859
):
    """
    Calculate the Clopper-Pearson confidence_level interval for a binomial proportion.
    
    Parameters:
        passed (int): Number of successes.
        total (int): Total number of trials.
        confidence_level (float): Confidence level (default is 1 sigma).
        
    Returns:
        tuple: (efficiency, efficiency error up, efficiency error low)
    """
    efficiency = passed/total

    alpha = 1 - confidence_level
    lower_bound = beta.ppf(alpha / 2, passed, total - passed + 1)
    upper_bound = beta.ppf(1 - alpha / 2, passed + 1, total - passed)
    
    return efficiency, abs(efficiency - upper_bound), abs(efficiency - lower_bound)




def bayesian_interval(
    passed:           float | int,
    total:            float | int,
    alpha_prior:      float = 1,
    beta_prior:       float = 1,
    confidence_level: float = 0.6826894921370859
):
    """
    Calculate the Bayesian credible interval for a binomial proportion
    using weighted data, similar to ROOT's TEfficiency::Bayesian method.
    
    Parameters:
        passed (float): Weighted number of successes.
        total (float): Weighted total number of trials.
        alpha_prior (float): Alpha parameter of the Beta prior distribution (default is 1 for uniform prior).
        beta_prior (float): Beta parameter of the Beta prior distribution (default is 1 for uniform prior).
        confidence_level (float): Confidence level (default is 1 sigma).
        
    Returns:
        tuple: (efficiency, efficiency error up, efficiency error low)
    """
    # Posterior parameters for Beta distribution
    alpha_post = alpha_prior + passed
    beta_post = beta_prior + total - passed
    
    # Calculate credible interval
    lower_bound = beta.ppf((1 - confidence_level) / 2, alpha_post, beta_post)
    upper_bound = beta.ppf(1 - (1 - confidence_level) / 2, alpha_post, beta_post)
    efficiency = passed/total

    return efficiency, abs(efficiency - upper_bound), abs(efficiency - lower_bound)