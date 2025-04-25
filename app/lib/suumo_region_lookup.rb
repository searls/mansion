# frozen_string_literal: true

require "json"

class SuumoRegionLookup
  SUFFIXES = /[市県町区村郡]$/

  def initialize(json_path)
    @lookup = JSON.parse(File.read(json_path))
  end

  def find_region_code(keyword)
    # Direct match
    @lookup.each do |code, entry|
      return code if entry["keywords"].include?(keyword)
    end
    # Try base match
    base = keyword.sub(SUFFIXES, "")
    candidates = @lookup.select { |_code, entry| entry["keywords"].any? { |k| base.present? && k.include?(base) } }.keys
    return candidates.first if candidates.size == 1
    raise "Could not find region for keyword: #{keyword}"
  end
end
