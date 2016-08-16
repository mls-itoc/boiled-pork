# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)

["広島県",
"岡山県",
"島根県",
"鳥取県",
"山口県",
"佐賀県",
"福岡県",
"熊本県",
"宮崎県",
"愛媛県",
"香川県",
"高知県",
"大分県",
"徳島県",
"愛知県",
"岐阜県",
"石川県",
"三重県",
"長野県",
"静岡県",
"富山県",
"北海道",
"福井県",
"兵庫県",
"京都府",
"奈良県",
"大阪府",
"滋賀県",
"和歌山県",
"千葉県",
"茨城県",
"神奈川県",
"埼玉県",
"栃木県",
"東京都",
"山梨県",
"秋田県",
"青森県",
"福島県",
"岩手県",
"宮城県",
"新潟県",
"山形県",
"長崎県",
"鹿児島県",
"沖縄県",
"群馬県"].each_with_index do |p, i|
  Pref.find_or_create_by(id: i + 1, name: p)
end
