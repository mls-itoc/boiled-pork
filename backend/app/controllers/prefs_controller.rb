class PrefsController < ApplicationController
  def index
    render json: Pref.all.map { |p| [p.name, p.id] }.to_h.to_json
  end
end
