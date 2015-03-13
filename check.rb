require "listen"

module FileTracker
  filedir = "./img"

  # Should only track 'file1' and 'file2' in this directory
  listener = Listen.to(filedir, :force_polling=>true) do |modified, added, removed|
    puts "Updated: " + modified.first
  end
  listener.start
  sleep
end

