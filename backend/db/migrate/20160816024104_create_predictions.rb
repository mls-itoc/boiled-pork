class CreatePredictions < ActiveRecord::Migration[5.0]
  def change
    create_table :predictions do |t|
      t.date :date
      t.integer :yellow_dust, default: 0
      t.references :pref
    end
  end
end
