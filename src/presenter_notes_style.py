"""Presenter-only styling for the hidden defense cue cards.

This module is intentionally isolated from the audience-facing dashboard so
changes to rehearsal readability never alter the visible thesis presentation.
"""

PRESENTER_NOTES_CSS = """
<style>
  [data-testid="stAppViewContainer"]{background:#071525!important}
  [data-testid="stAppViewContainer"] .block-container{max-width:1320px!important;padding:2.8rem 3.6rem!important}

  [data-testid="stAppViewContainer"] .presenter-heading{
    font-family:Arial,sans-serif!important;
    font-size:2.7rem!important;
    font-weight:800!important;
    line-height:1.16!important;
    color:#72cfff!important;
    margin:0 0 2.5rem!important;
  }

  [data-testid="stAppViewContainer"] .presenter-copy{
    font-family:Arial,sans-serif!important;
    font-size:1.78rem!important;
    line-height:1.62!important;
    color:#f4f8ff!important;
  }

  [data-testid="stAppViewContainer"] .presenter-section{margin:0 0 3.1rem!important}

  [data-testid="stAppViewContainer"] .presenter-copy .presenter-section h2{
    font-size:1.55rem!important;
    letter-spacing:.12em!important;
    color:#72cfff!important;
    margin:0 0 1rem!important;
  }

  [data-testid="stAppViewContainer"] .presenter-section p{margin:0!important}

  [data-testid="stAppViewContainer"] .presenter-section ul{
    margin:.2rem 0 0 1.55rem!important;
    padding:0!important;
  }

  [data-testid="stAppViewContainer"] .presenter-section li{
    margin:0 0 1rem!important;
    padding-left:.2rem!important;
  }

  [data-testid="stAppViewContainer"] .presenter-section li ul{
    margin:.6rem 0 .35rem 1.55rem!important;
    color:#c9daeb!important;
    font-size:1.62rem!important;
    line-height:1.58!important;
  }

  @media (max-width: 1100px){
    [data-testid="stAppViewContainer"] .block-container{padding:2.2rem 2.5rem!important}
    [data-testid="stAppViewContainer"] .presenter-heading{font-size:2.35rem!important}
    [data-testid="stAppViewContainer"] .presenter-copy{font-size:1.58rem!important}
    [data-testid="stAppViewContainer"] .presenter-section li ul{font-size:1.46rem!important}
  }
</style>
"""
