"""Educational TV ultimate revision and recoverability screen; USD millions.

This is an illustrative prospective revenue-ratio model, not an IFRS valuation.
"""
import copy
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def load():
    data=json.loads((ROOT/'data/assumptions.json').read_text()); validate(data); return data


def validate(a):
    required=['opening_unamortized_cost','current_additions','historical_revenue',
              'historical_production_cost','historical_other_cost','current_revenue',
              'current_exploitation_cost','future_exploitation_cost','participation_rate']
    for k in required:
        if not isinstance(a.get(k),(int,float)) or a[k]<0: raise ValueError(f'Invalid {k}')
    if a['opening_unamortized_cost']>a['historical_production_cost']:
        raise ValueError('Opening carrying cost exceeds historical capitalized cost')
    if not 0<=a['participation_rate']<=1: raise ValueError('Participation rate outside 0-1')
    windows=a['windows']
    if not windows or len({r['window'] for r in windows})!=len(windows): raise ValueError('Duplicate or missing window')
    for r in windows:
        if any(r[k]<0 for k in ('prior_future_revenue','revised_future_revenue')): raise ValueError('Negative revenue')


def calculate(a, revision='revised', haircut=0):
    validate(a)
    if revision not in ('prior','revised') or not 0<=haircut<=1: raise ValueError('Invalid scenario')
    future=sum(r[f'{revision}_future_revenue'] for r in a['windows'])*(1-haircut)
    remaining=a['current_revenue']+future
    available=a['opening_unamortized_cost']+a['current_additions']
    # Screen BEFORE amortization; negative net proceeds cannot support an asset.
    net_proceeds=max(0,remaining*(1-a['participation_rate'])-a['current_exploitation_cost']-a['future_exploitation_cost'])
    screen_write_down=max(0,available-net_proceeds)
    ratio=a['current_revenue']/remaining if remaining>0 else 0
    amortization=(available-screen_write_down)*ratio
    closing=available-screen_write_down-amortization
    current_contribution=a['current_revenue']*(1-a['participation_rate'])-a['current_exploitation_cost']-amortization-screen_write_down
    lifetime_revenue=a['historical_revenue']+remaining
    # Historical other cost already includes historical participation: don't count it twice.
    lifetime_contribution=lifetime_revenue-a['historical_production_cost']-a['current_additions']-a['historical_other_cost']-a['current_exploitation_cost']-a['future_exploitation_cost']-remaining*a['participation_rate']
    break_even_future=max(0,(available+a['current_exploitation_cost']+a['future_exploitation_cost'])/(1-a['participation_rate'])-a['current_revenue']) if a['participation_rate']<1 else None
    return dict(future_revenue=future,remaining_revenue=remaining,lifetime_revenue=lifetime_revenue,
                available_cost=available,net_remaining_proceeds=net_proceeds,recoverability_headroom=net_proceeds-available,
                illustrative_write_down=screen_write_down,revenue_ratio=ratio,amortization=amortization,
                closing_content_asset=closing,current_contribution=current_contribution,
                lifetime_contribution=lifetime_contribution,break_even_future_revenue=break_even_future,
                rollforward_error=available-screen_write_down-amortization-closing)


def main():
    a=load()
    cases={'prior':calculate(a,'prior'),'revised':calculate(a),
           'downside':calculate(a,haircut=a['downside_future_revenue_haircut']),
           'stress':calculate(a,haircut=a['stress_future_revenue_haircut'])}
    results=ROOT/'results'; results.mkdir(exist_ok=True)
    (results/'metrics.json').write_text(json.dumps(cases,indent=2)+'\n')
    with (results/'sensitivity.csv').open('w',newline='') as f:
        fields=['haircut','future_revenue','current_contribution','illustrative_write_down','closing_content_asset']
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for h in range(0,101,5):
            m=calculate(a,haircut=h/100); w.writerow({'haircut':h/100,**{k:m[k] for k in fields[1:]}})
    print(json.dumps(cases,indent=2))


if __name__=='__main__': main()
