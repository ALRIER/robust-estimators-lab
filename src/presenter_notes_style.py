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

  [data-testid="stAppViewContainer"] .presenter-help-list{
    margin:.35rem 0 0 1.7rem!important;
    padding:0!important;
    max-width:1180px!important;
  }

  [data-testid="stAppViewContainer"] .presenter-help-list li{
    margin:0 0 1.25rem!important;
    padding-left:.35rem!important;
    line-height:1.55!important;
  }

  [data-testid="stAppViewContainer"] .presenter-help-list li::marker{
    color:#f3c743!important;
    font-size:1.08em!important;
  }

  [data-testid="stAppViewContainer"] .presenter-formulas{
    margin-top:.4rem!important;
  }

  [data-testid="stAppViewContainer"] .presenter-formula-card{
    margin:0 0 2.2rem!important;
    padding:1.25rem 1.45rem 1.15rem!important;
    border:1px solid #2f6d98!important;
    border-left:5px solid #f3c743!important;
    border-radius:10px!important;
    background:#0a1d32!important;
  }

  [data-testid="stAppViewContainer"] .presenter-formula-title{
    font-size:1.32rem!important;
    line-height:1.25!important;
    font-weight:800!important;
    color:#72cfff!important;
    margin:0 0 .55rem!important;
  }

  [data-testid="stAppViewContainer"] .presenter-formula-expression{
    font-family:Georgia,'Times New Roman',serif!important;
    font-size:2rem!important;
    line-height:1.35!important;
    font-weight:700!important;
    color:#f3c743!important;
    margin:0 0 1rem!important;
    overflow-wrap:anywhere!important;
  }

  [data-testid="stAppViewContainer"] .presenter-formula-parts{
    margin:.35rem 0 0 1.65rem!important;
    padding:0!important;
  }

  [data-testid="stAppViewContainer"] .presenter-formula-parts li{
    margin:0 0 .9rem!important;
    padding-left:.25rem!important;
    line-height:1.5!important;
  }

  [data-testid="stAppViewContainer"] .presenter-formula-parts li::marker{
    color:#72cfff!important;
  }

  [data-testid="stAppViewContainer"] .presenter-formula-parts strong{
    color:#ffffff!important;
    font-weight:800!important;
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
    [data-testid="stAppViewContainer"] .presenter-formula-expression{font-size:1.75rem!important}
    [data-testid="stAppViewContainer"] .presenter-section li ul{font-size:1.46rem!important}
  }
</style>
"""
