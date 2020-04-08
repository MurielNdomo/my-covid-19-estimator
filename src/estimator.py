def estimator(data):
  reportedCases = data['reportedCases']
  periodType, timeToElapse = data['periodType'], data['timeToElapse']
  return dict(
    data=data, 
    impact=computeImpact(reportedCases, impactEstimator, periodType, timeToElapse), 
    severeImpact=computeImpact(reportedCases, severeImpactEstimator, periodType, timeToElapse)
  )

def computeImpact(reportedCases, estimatorMethod, periodType, timeToElapse):
  currentlyInfected = estimatorMethod(reportedCases)
  return dict(
    currentlyInfected=currentlyInfected,
    infectionsByRequestedTime=computeInfectionsByRequestedTime(currentlyInfected, periodType, timeToElapse)
  )
def normalizeDuration(periodType, timeToElapse):
  """Returns number of days given periodType and timeToElapse"""
  if periodType == "weeks":
    return timeToElapse*7
  if periodType == "months":
    return timeToElapse*30
  return timeToElapse

def computeInfectionsByRequestedTime(currentlyInfected, periodType, timeToElapse):
  return currentlyInfected*(2**(normalizeDuration(periodType,timeToElapse)//3))


def impactEstimator(reportedCases):
  return reportedCases*10

def severeImpactEstimator(reportedCases):
  return reportedCases*50