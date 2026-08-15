"""Presenter-only styling for the hidden defense cue cards.

This module is intentionally isolated from the audience-facing dashboard so
changes to rehearsal readability never alter the visible thesis presentation.
"""

PRESENTER_NOTES_CSS = """
<style>
  [data-testid="stAppViewContainer"]{background:#071525!important}
  .block-container{max-width:1320px!important;padding:2.8rem 3.6rem!important}

  .presenter-heading{
    font-family:Arial,sans-serif;
    font-size:2.7rem;
    font-weight:800;
    line-height:1.16;
    color:#72cfff;
    margin:0 0 2.5rem;
  }

  .presenter-copy{
    font-family:Arial,sans-serif;
    font-size:1.78rem;
    line-height:1.62;
    color:#f4f8ff;
  }

  .presenter-section{margin:0 0 3.1rem}

  .presenter-section h2{
    font-size:1.38rem!important;
    letter-spacing:.12em;
    color:#72cfff!important;
    margin:0 0 1rem!important;
  }

  .presenter-section p{margin:0}

  .presenter-section ul{
    margin:.2rem 0 0 1.55rem;
    padding:0;
  }

  .presenter-section li{
    margin:0 0 1rem;
    padding-left:.2rem;
  }

  .presenter-section li ul{
    margin:.6rem 0 .35rem 1.55rem;
    color:#c9daeb;
    font-size:1.62rem;
    line-height:1.58;
  }

  @media (max-width: 1100px){
    .block-container{padding:2.2rem 2.5rem!important}
    .presenter-heading{font-size:2.35rem}
    .presenter-copy{font-size:1.58rem}
    .presenter-section li ul{font-size:1.46rem}
  }
</style>
"""
