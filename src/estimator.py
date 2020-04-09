def estimator(data):
  reportedCases = data['reportedCases']
  periodType, timeToElapse, totalHospitalBeds = data['periodType'], data['timeToElapse'], data['totalHospitalBeds']
  return dict(
    data=data, 
    impact=computeImpact(reportedCases, impactEstimator, periodType, timeToElapse, totalHospitalBeds), 
    severeImpact=computeImpact(reportedCases, severeImpactEstimator, periodType, timeToElapse, totalHospitalBeds)
  )

def computeImpact(reportedCases, estimatorMethod, periodType, timeToElapse, totalHospitalBeds):
  currentlyInfected = estimatorMethod(reportedCases)
  infectionsByRequestedTime = computeInfectionsByRequestedTime(currentlyInfected, periodType, timeToElapse)
  severeCasesByRequestedTime=computeSevereCasesByRequestedTime(infectionsByRequestedTime)
  return dict(
    currentlyInfected=currentlyInfected,
    infectionsByRequestedTime=infectionsByRequestedTime,
    severeCasesByRequestedTime=severeCasesByRequestedTime,
    hospitalBedsByRequestedTime=computeHospitalBedsByRequestedTime(severeCasesByRequestedTime, totalHospitalBeds)
  )
def computeHospitalBedsByRequestedTime(severeCasesByRequestedTime, totalHospitalBeds):
  return float(int((35*totalHospitalBeds)/100 - severeCasesByRequestedTime))

def computeSevereCasesByRequestedTime(infectionsByRequestedTime):
  return float(int((infectionsByRequestedTime*15)/100))

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