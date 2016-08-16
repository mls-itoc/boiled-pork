class PredictionController < ApplicationController
  def index
  end

  def fetch_prediction
    prediction = Prediction.fetch_with_date(params[:date])
    render json: prediction.try(:to_json)
  end
end
