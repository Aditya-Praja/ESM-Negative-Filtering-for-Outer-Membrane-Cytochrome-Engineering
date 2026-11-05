"""Phase 2: regress ESM site tolerance on structural covariates ONLY; keep the residual.

y_i = llr_mean_across_subs. Covariates: rsa_holo, f(d_fe), f(d_porph), ss, domain.
f(d) = exp(-d/4 A). OLS first; GAM only if residuals curve. NO random forest.
Residuals are spatially autocorrelated -> descriptive only, or spatial block bootstrap.
Large negative residual = functional conservation = engineering TARGET, not exclusion.
Figure: residual vs position, colored by domain, chemistry-mask positions marked,
known functional regions shaded -> reports/figures/residual.png
"""


def main():
    raise NotImplementedError


if __name__ == "__main__":
    main()
