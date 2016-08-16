class Prediction < ApplicationRecord
  belongs_to :pref
  class << self
    def fetch_with_date(date)
      date = Date.parse(date)
      ps = self.where(date: date)
      hash = ps.reduce({}) do |res, p|
        res[p.pref_id] = p.yellow_dust
        res
      end
      Pref.all.each do |p|
        unless hash.has_key?(p.id)
          hash[p.id] = 0
        end
      end
      return hash
    end
  end
end
