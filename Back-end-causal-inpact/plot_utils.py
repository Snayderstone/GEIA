import pandas as pd

def plot2(self, path, panels=['original', 'pointwise', 'cumulative'], figsize=(15, 12)):
    """Plots inferences results related to causal impact analysis.

    Args
    ----
      panels: list.
        Indicates which plot should be considered in the graphics.
      figsize: tuple.
        Changes the size of the graphics plotted.

    Raises
    ------
      RuntimeError: if inferences were not computed yet.
    """
    plt = self._get_plotter()
    fig = plt.figure(figsize=figsize)
    if self.summary_data is None:
        raise RuntimeError('Please first run inferences before plotting results')

    valid_panels = ['original', 'pointwise', 'cumulative']
    for panel in panels:
        if panel not in valid_panels:
            raise ValueError(
                '"{}" is not a valid panel. Valid panels are: {}.'.format(
                    panel, ', '.join(['"{}"'.format(e) for e in valid_panels])
                )
            )

    llb = self.trained_model.filter_results.loglikelihood_burn
    inferences = self.inferences.iloc[llb:]

    intervention_idx = inferences.index.get_loc(self.post_period[0])
    n_panels = len(panels)
    ax = plt.subplot(n_panels, 1, 1)
    idx = 1

    if 'original' in panels:
        ax.plot(pd.concat([self.pre_data.iloc[llb:, 0], self.post_data.iloc[:, 0]]),
                'k', label='y')
        ax.plot(inferences['preds'], 'b--', label='Predicted')
        ax.axvline(inferences.index[intervention_idx - 1], c='k', linestyle='--')
        ax.fill_between(
            self.pre_data.index[llb:].union(self.post_data.index),
            inferences['preds_lower'],
            inferences['preds_upper'],
            facecolor='blue',
            interpolate=True,
            alpha=0.25
        )
        ax.grid(True, linestyle='--')
        ax.legend()
        if idx != n_panels:
            plt.setp(ax.get_xticklabels(), visible=False)
        idx += 1

    if 'pointwise' in panels:
        ax = plt.subplot(n_panels, 1, idx, sharex=ax)
        ax.plot(inferences['point_effects'], 'b--', label='Point Effects')
        ax.axvline(inferences.index[intervention_idx - 1], c='k', linestyle='--')
        ax.fill_between(
            inferences['point_effects'].index,
            inferences['point_effects_lower'],
            inferences['point_effects_upper'],
            facecolor='blue',
            interpolate=True,
            alpha=0.25
        )
        ax.axhline(y=0, color='k', linestyle='--')
        ax.grid(True, linestyle='--')
        ax.legend()
        if idx != n_panels:
            plt.setp(ax.get_xticklabels(), visible=False)
        idx += 1

    if 'cumulative' in panels:
        ax = plt.subplot(n_panels, 1, idx, sharex=ax)
        ax.plot(inferences['post_cum_effects'], 'b--',
                label='Cumulative Effect')
        ax.axvline(inferences.index[intervention_idx - 1], c='k', linestyle='--')
        ax.fill_between(
            inferences['post_cum_effects'].index,
            inferences['post_cum_effects_lower'],
            inferences['post_cum_effects_upper'],
            facecolor='blue',
            interpolate=True,
            alpha=0.25
        )
        ax.grid(True, linestyle='--')
        ax.axhline(y=0, color='k', linestyle='--')
        ax.legend()

    if llb > 0:
        text = ('Note: The first {} observations were removed due to approximate '
                'diffuse initialization.'.format(llb))
        fig.text(0.1, 0.01, text, fontsize='large')

    plt.savefig(path)
