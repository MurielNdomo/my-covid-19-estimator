def estimator(data):
  return dict(
    data=data, 
    impact=computeImpact(impactEstimator, data), 
    severeImpact=computeImpact(severeImpactEstimator, data)
  )

def computeImpact(estimatorMethod, data):
  reportedCases, periodType, timeToElapse, totalHospitalBeds = data['reportedCases'], data['periodType'], data['timeToElapse'], data['totalHospitalBeds']
  region = data['region']
  avgDailyIncome, avgDailyIncomePopulation = region['avgDailyIncomeInUSD'], region['avgDailyIncomePopulation']
  numberOfDays = normalizeDuration(periodType,timeToElapse)
  currentlyInfected = estimatorMethod(reportedCases)
  infectionsByRequestedTime = computeInfectionsByRequestedTime(currentlyInfected, numberOfDays)
  severeCasesByRequestedTime= computeInfectionTypeRate(infectionsByRequestedTime, 15)
  return dict(
    currentlyInfected=currentlyInfected,
    infectionsByRequestedTime=infectionsByRequestedTime,
    severeCasesByRequestedTime=severeCasesByRequestedTime,
    hospitalBedsByRequestedTime=computeHospitalBedsByRequestedTime(severeCasesByRequestedTime, totalHospitalBeds),
    casesForICUByRequestedTime=computeInfectionTypeRate(infectionsByRequestedTime, 5),
    casesForVentilatorsByRequestedTime=computeInfectionTypeRate(infectionsByRequestedTime, 2),
    dollarsInFlight=computeDollarsInFlight(avgDailyIncome, avgDailyIncomePopulation, numberOfDays, infectionsByRequestedTime)
  )
def computeDollarsInFlight(avgDailyIncome, avgDailyIncomePopulation ,numberOfDays, infectionsByRequestedTime):
  return round(infectionsByRequestedTime * avgDailyIncomePopulation * avgDailyIncome * numberOfDays, 2)

def computeHospitalBedsByRequestedTime(severeCasesByRequestedTime, totalHospitalBeds):
  return float(int((35*totalHospitalBeds)/100 - severeCasesByRequestedTime))

def computeInfectionTypeRate(infections, rate):
  return float(int((infections*rate)/100))

def normalizeDuration(periodType, timeToElapse):
  """Returns number of days given periodType and timeToElapse"""
  if periodType == "weeks":
    return timeToElapse*7
  if periodType == "months":
    return timeToElapse*30
  return timeToElapse

def computeInfectionsByRequestedTime(currentlyInfected, numberOfDays):
  return currentlyInfected*(2**(numberOfDays//3))


def impactEstimator(reportedCases):
  return reportedCases*10

def severeImpactEstimator(reportedCases):
  return reportedCases*50