// Civilization Models: What Each Gate Produces at 75-Year Scale
// Each quiz answer (correct and wrong) produces a civilization outcome

const civilizationModels = {
  // GATE 1: AGENCY VS CIRCUMSTANCE
  gate_1_business: {
    correctAnswerCiv: {
      title: "Business Civilization: Own Your Agency",
      timespan: "75 years of operation",
      population: 1000,
      cities_healthy: 943,
      cities_struggling: 57,
      metrics: {
        life_expectancy: { value: 84, baseline: 78 },
        infant_mortality: { value: 0.8, baseline: 1.2 },
        economic_mobility: { value: 3.1, baseline: 0 },
        gdp_growth: { value: 2.8, baseline: 2.0 },
        ecosystem_health: { value: "91% stable", baseline: "75% declining" },
        governance_stability: { value: "1 smooth transition", baseline: "varies" },
        population_satisfaction: { value: "87%", baseline: "45%" },
        collapse_risk: { value: "4%", baseline: "50%" }
      },
      features: [
        "Firms take ownership of failures, learn from them, improve systems",
        "Economic decisions improve iteratively (we caused this, we can fix it)",
        "Innovation accelerates (failure = learning, not blame)",
        "Resource allocation matches actual responsibility areas",
        "Governance coherence: leaders own outcomes they influence",
        "Cascading improvement: ownership -> learning -> system improvement"
      ],
      visual: {
        color_distribution: "943 green, 57 yellow, 0 red",
        pattern: "Clusters of prosperity with pockets of managed challenges",
        worst_city: "Still functioning, still improving",
        best_city: "Thriving, innovating, attracting talent"
      }
    },
    wrongAnswerCiv_Victim: {
      title: "Business Civilization: Everything Happens To You",
      timespan: "75 years of operation",
      population: 1000,
      cities_healthy: 124,
      cities_struggling: 687,
      cities_collapsed: 189,
      metrics: {
        life_expectancy: { value: 61, baseline: 78 },
        infant_mortality: { value: 8.9, baseline: 1.2 },
        economic_mobility: { value: -2.3, baseline: 0 },
        gdp_growth: { value: -0.4, baseline: 2.0 },
        ecosystem_health: { value: "19% critical failures", baseline: "75% stable" },
        governance_stability: { value: "12 regime changes", baseline: "1-2" },
        population_satisfaction: { value: "18%", baseline: "45%" },
        collapse_risk: { value: "89%", baseline: "50%" }
      },
      features: [
        "Firms blame market conditions, can't improve what they don't control",
        "Innovation stops (failures are 'bad luck', not learning opportunities)",
        "Scapegoating becomes default (it's never us, it's always them)",
        "Resource allocation becomes political (blame-shifting for power)",
        "Governance collapse (nobody owns anything, everyone blames)",
        "Cascading decay: no ownership -> no learning -> system breakdown"
      ],
      visual: {
        color_distribution: "124 green, 687 yellow, 189 red",
        pattern: "Pockets of relative stability surrounded by chaos and collapse",
        worst_city: "Abandoned, governance failure, population fled",
        best_city: "Barely functional, slow decline, resignation visible"
      }
    },
    wrongAnswerCiv_Blame: {
      title: "Business Civilization: It's Always Someone Else's Fault",
      timespan: "75 years of operation",
      population: 1000,
      cities_healthy: 89,
      cities_struggling: 512,
      cities_collapsed: 399,
      metrics: {
        life_expectancy: { value: 54, baseline: 78 },
        infant_mortality: { value: 14.2, baseline: 1.2 },
        economic_mobility: { value: -4.1, baseline: 0 },
        gdp_growth: { value: -1.8, baseline: 2.0 },
        ecosystem_health: { value: "8% critical, 67% toxic", baseline: "75% stable" },
        governance_stability: { value: "23 regime changes", baseline: "1-2" },
        population_satisfaction: { value: "8%", baseline: "45%" },
        collapse_risk: { value: "96%", baseline: "50%" }
      },
      features: [
        "Firms locked in blame cycles with external parties",
        "Innovation impossible (enemies can't be trusted, cooperation blocked)",
        "Economic warfare replaces cooperation (everyone fighting everyone)",
        "Resource hoarding and depletion (if we don't take it, enemy will)",
        "Governance collapse through blame loops (all leaders replaced in chaos)",
        "Civilizational breakdown: no cooperation -> no coordination -> collapse"
      ],
      visual: {
        color_distribution: "89 green, 512 yellow, 399 red",
        pattern: "Chaos and collapse scattered throughout",
        worst_city: "Warlord territory, infrastructure destroyed, population displaced",
        best_city: "Fortified enclave, isolated, declining from within"
      }
    }
  },

  // GATE 3: SIGNAL VS SYMPTOM (QUICK EXAMPLE)
  gate_3_business: {
    correctAnswerCiv: {
      title: "System Health: Distinguish Root Cause from Symptom",
      timespan: "75 years of operation",
      population: 1000,
      cities_healthy: 967,
      cities_struggling: 33,
      metrics: {
        life_expectancy: { value: 86, baseline: 78 },
        infant_mortality: { value: 0.6, baseline: 1.2 },
        economic_mobility: { value: 4.2, baseline: 0 },
        cascade_failures: { value: "2 (managed)", baseline: "47 (uncontrolled)" },
        governance_stability: { value: "Perfect", baseline: "varies" },
        population_satisfaction: { value: "92%", baseline: "45%" },
        collapse_risk: { value: "2%", baseline: "50%" }
      },
      features: [
        "Problems solved at root, not symptoms",
        "Policies integrated - fixing one doesn't break another",
        "Resource allocation to actual root causes",
        "Adaptive governance - systems learn and improve",
        "Resilience through coherence - systems support each other"
      ],
      visual: {
        color_distribution: "967 green, 33 yellow, 0 red",
        worst_city: "Still thriving, minor optimization happening"
      }
    },
    wrongAnswerCiv_LoudestSignal: {
      title: "System Health: Always Respond to Loudest Signal",
      timespan: "75 years of operation",
      population: 1000,
      cities_healthy: 153,
      cities_struggling: 647,
      cities_collapsed: 200,
      metrics: {
        life_expectancy: { value: 62, baseline: 78 },
        infant_mortality: { value: 9.1, baseline: 1.2 },
        economic_mobility: { value: -2.8, baseline: 0 },
        cascade_failures: { value: "847 uncontrolled cascades", baseline: "2-15" },
        governance_stability: { value: "Total breakdown", baseline: "varies" },
        population_satisfaction: { value: "31%", baseline: "45%" },
        collapse_risk: { value: "87%", baseline: "50%" }
      },
      features: [
        "Problems compound - fix one symptom, cause spreads elsewhere",
        "Resource thrashing - chasing loudest problem, ignoring root",
        "Governance chaos - different agencies fighting over which signal to follow",
        "Population suffering - needs aren't addressed, only visible symptoms",
        "System fragility - one shock causes total cascade failure"
      ],
      visual: {
        color_distribution: "153 green, 647 yellow, 200 red",
        pattern: "Chaos spread by cascading failures"
      }
    }
  }
};

// Helper function to get civilization for a specific gate/answer combination
function getCivilizationOutcome(gate, domain, answerCorrectness) {
  const key = `gate_${gate}_${domain.toLowerCase().replace(/\s/g, '_')}`;
  
  if (!civilizationModels[key]) {
    return generatePlaceholderCivilization(gate, domain, answerCorrectness);
  }
  
  if (answerCorrectness === 'correct') {
    return civilizationModels[key].correctAnswerCiv;
  } else {
    // Return a wrong answer civilization (could be multiple types)
    const wrongKeys = Object.keys(civilizationModels[key]).filter(k => k.startsWith('wrongAnswerCiv'));
    const randomWrong = wrongKeys[Math.floor(Math.random() * wrongKeys.length)];
    return civilizationModels[key][randomWrong];
  }
}

function generatePlaceholderCivilization(gate, domain, correctness) {
  if (correctness === 'correct') {
    return {
      title: `Civilization Operating on Gate ${gate} Understanding (${domain})`,
      timespan: "75 years of operation",
      population: 1000,
      cities_healthy: 945 - (gate * 5),
      cities_struggling: 45 + (gate * 3),
      metrics: {
        life_expectancy: { value: 85 - (gate * 0.5), baseline: 78 },
        economic_mobility: { value: 3.5 - (gate * 0.2), baseline: 0 },
        collapse_risk: { value: `${3 + (gate * 1)}%`, baseline: "50%" }
      },
      features: [
        `Gate ${gate} comprehension enables ${domain} systems to function coherently`,
        "Cascading improvements across related domains",
        "Governance stability and population wellbeing increase",
        "System resilience and adaptability improve"
      ],
      visual: {
        color_distribution: `${945 - (gate * 5)} green, ${45 + (gate * 3)} yellow, 0 red`
      }
    };
  } else {
    return {
      title: `Civilization Without Gate ${gate} Understanding (${domain})`,
      timespan: "75 years of operation",
      population: 1000,
      cities_healthy: 150 + (gate * 20),
      cities_struggling: 500 + (gate * 15),
      cities_collapsed: 350 - (gate * 35),
      metrics: {
        life_expectancy: { value: 62 + (gate * 2), baseline: 78 },
        economic_mobility: { value: -2.5 + (gate * 0.3), baseline: 0 },
        collapse_risk: { value: `${85 - (gate * 5)}%`, baseline: "50%" }
      },
      features: [
        `Absence of Gate ${gate} understanding creates cascading failures in ${domain}`,
        "System dysfunction spreads across dependent domains",
        "Governance breakdown and population suffering",
        "Collapse risk increases exponentially"
      ],
      visual: {
        color_distribution: `${150 + (gate * 20)} green, ${500 + (gate * 15)} yellow, ${350 - (gate * 35)} red`
      }
    };
  }
}

// Export for use in game-engine.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { civilizationModels, getCivilizationOutcome };
}
